"""Construction des requêtes et assemblage des résultats en tableaux.

Ce module transforme les arguments des fonctions publiques en une ou
plusieurs requêtes HTTP, puis assemble les enregistrements obtenus en
``DataFrame`` (pandas ou polars) ou en ``GeoDataFrame``.

Règles appliquées aux paramètres de localisation, par ordre de priorité :

1. ``lon_lat`` : point contenu dans les objets renvoyés ;
2. ``in_bbox`` : emprise rectangulaire ``[lon_min, lat_min, lon_max, lat_max]`` ;
3. ``code_insee`` : codes communaux, regroupés par lots de 10 par requête ;
4. ``code`` : codes géographiques des indicateurs, regroupés par lots de 10 ;
5. ``coddep`` : codes départementaux, une requête par code.

Si plusieurs paramètres de localisation sont fournis, seul le plus prioritaire
est utilisé et un avertissement est émis.
"""

from __future__ import annotations

import json
import math
import re
import warnings
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple, Union
from urllib.parse import quote

import geopandas as gpd
import pandas as pd
from tqdm import tqdm

from . import config
from ._http import get_api_response, iter_pages
from .exceptions import ValidationError

LOCATION_KEYS = ("lon_lat", "in_bbox", "code_insee", "code", "coddep")
MAX_CODES_PER_REQUEST = 10
LON_LAT_HALF_SIZE = 0.01
CRS = "EPSG:4326"

# Emprise maximale autorisée par l'API (degrés), selon la famille d'endpoints.
BBOX_MAX_DEFAULT = 0.02
BBOX_MAX_CARTOFRICHES = 1.0

# Caractères admis dans un code ou un identifiant : alphanumériques et « + * _ - »
# (les comptes communaux des Fichiers fonciers contiennent par exemple « + »).
_CODE_PATTERN = re.compile(r"^[0-9A-Za-z+*_-]+$")

Table = Any  # pandas.DataFrame ou polars.DataFrame selon OUTPUT_FORMAT

# Alias de types utilisés dans les signatures publiques.
Codes = Optional[Union[str, Sequence[str]]]
BBox = Optional[Sequence[float]]
Point = Optional[Sequence[float]]
Multi = Optional[Union[str, Sequence[str]]]


def is_num(value: Any) -> bool:
    """Indique si une valeur est un nombre réel fini (booléens exclus).

    Args:
        value: Valeur à tester.

    Returns:
        ``True`` pour un ``int`` ou un ``float`` fini.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    return math.isfinite(value)


def as_list(value: Union[str, int, Iterable[Any]]) -> List[str]:
    """Normalise une valeur scalaire ou itérable en liste de chaînes.

    Args:
        value: Chaîne, entier ou itérable de valeurs.

    Returns:
        La liste des valeurs converties en chaînes, sans espaces superflus.
    """
    if isinstance(value, (str, int)):
        items = [value]
    else:
        items = list(value)
    return [str(item).strip() for item in items]


def check_code(code: str, name: str) -> str:
    """Vérifie qu'un code ou identifiant ne contient que des caractères admis.

    Ce contrôle empêche qu'un identifiant inséré dans le chemin d'une URL
    (``/ff/parcelles/<idpar>/``) ne détourne la requête vers une autre ressource.

    Args:
        code: Code à contrôler.
        name: Nom du paramètre, pour le message d'erreur.

    Returns:
        Le code contrôlé.

    Raises:
        ValidationError: Si le code est vide ou contient d'autres caractères.
    """
    if not code or not _CODE_PATTERN.fullmatch(code):
        raise ValidationError(
            f"{name} invalide : {code!r} (caractères admis : lettres, chiffres, + * _ -)."
        )
    return code


def path_segment(value: Any, name: str) -> str:
    """Prépare un identifiant pour son insertion dans un chemin d'URL.

    Args:
        value: Identifiant fourni par l'utilisateur.
        name: Nom du paramètre, pour le message d'erreur.

    Returns:
        L'identifiant contrôlé et encodé pour l'URL.

    Raises:
        ValidationError: Si l'identifiant est absent ou invalide.
    """
    if value is None:
        raise ValidationError(f"Le paramètre {name} est obligatoire.")
    return quote(check_code(str(value).strip(), name), safe="")


def chunks(items: Sequence[str], size: int) -> List[List[str]]:
    """Découpe une liste en lots de taille bornée.

    Args:
        items: Éléments à découper.
        size: Taille maximale d'un lot.

    Returns:
        La liste des lots.
    """
    return [list(items[i : i + size]) for i in range(0, len(items), size)]


def clean_params(params: Mapping[str, Any]) -> Dict[str, Any]:
    """Retire les valeurs ``None`` et sérialise les listes et booléens.

    Args:
        params: Paramètres bruts.

    Returns:
        Les paramètres prêts à être transmis dans la chaîne de requête.
    """
    cleaned: Dict[str, Any] = {}
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, bool):
            cleaned[key] = str(value).lower()
        elif isinstance(value, (list, tuple, set)):
            cleaned[key] = ",".join(str(item).strip() for item in value)
        else:
            cleaned[key] = value
    return cleaned


def select_location(params: Dict[str, Any]) -> Tuple[str, Any]:
    """Extrait de ``params`` le paramètre de localisation à utiliser.

    Les clés de localisation sont retirées de ``params``.

    Args:
        params: Paramètres de l'appel, modifiés sur place.

    Returns:
        Le couple ``(nom, valeur)`` du paramètre retenu.

    Raises:
        ValidationError: Si aucun paramètre de localisation n'est fourni.
    """
    provided = {
        key: params.pop(key) for key in LOCATION_KEYS if params.get(key) is not None
    }
    for key in LOCATION_KEYS:
        params.pop(key, None)
    if not provided:
        raise ValidationError(
            "Veuillez préciser au moins un paramètre parmi "
            "lon_lat, in_bbox, code_insee, code et coddep."
        )
    first = next(key for key in LOCATION_KEYS if key in provided)
    if len(provided) > 1:
        warnings.warn(
            f"Les mots-clés {', '.join(provided)} ont été précisés. "
            f"Seul le mot-clé {first} sera utilisé.",
            UserWarning,
            stacklevel=4,
        )
    return first, provided[first]


def check_bbox(value: Any) -> Tuple[float, float, float, float]:
    """Valide une emprise rectangulaire.

    Args:
        value: Liste ``[lon_min, lat_min, lon_max, lat_max]``.

    Returns:
        L'emprise sous forme de quadruplet.

    Raises:
        ValidationError: Si l'emprise est mal formée, inversée ou hors bornes.
    """
    if (
        not isinstance(value, (list, tuple))
        or len(value) != 4
        or not all(is_num(x) for x in value)
    ):
        raise ValidationError("Le paramètre in_bbox doit être une liste de 4 floats.")
    lon_min, lat_min, lon_max, lat_max = value
    if lon_min >= lon_max or lat_min >= lat_max:
        raise ValidationError(
            "Le paramètre in_bbox doit respecter lon_min < lon_max et lat_min < lat_max."
        )
    if not (-180 <= lon_min and lon_max <= 180 and -90 <= lat_min and lat_max <= 90):
        raise ValidationError("Le paramètre in_bbox sort des bornes géographiques.")
    return lon_min, lat_min, lon_max, lat_max


def _edges(start: float, stop: float, step: float) -> List[Tuple[float, float]]:
    """Découpe un intervalle en segments de longueur au plus ``step``.

    Args:
        start: Borne inférieure.
        stop: Borne supérieure.
        step: Longueur maximale d'un segment.

    Returns:
        La liste des segments ``(début, fin)``, arrondis au millionième de degré.
    """
    count = max(1, math.ceil((stop - start) / step - 1e-9))
    inner = [round(start + i * step, 6) for i in range(1, count)]
    bounds = [start, *inner, stop]
    return list(zip(bounds[:-1], bounds[1:]))


def tile_bbox(value: Any, max_size: Optional[float]) -> List[str]:
    """Valide une emprise et la découpe en tuiles respectant la taille maximale.

    Une emprise qui respecte déjà la limite donne une seule tuile.

    Args:
        value: Liste ``[lon_min, lat_min, lon_max, lat_max]``.
        max_size: Largeur et hauteur maximales d'une tuile en degrés
            (``None`` : pas de découpage).

    Returns:
        Les tuiles au format ``"lon_min,lat_min,lon_max,lat_max"``.

    Raises:
        ValidationError: Si l'emprise est invalide ou si le nombre de tuiles
            dépasse ``MAX_TILES``.
    """
    lon_min, lat_min, lon_max, lat_max = check_bbox(value)
    if max_size is None or (
        lon_max - lon_min <= max_size + 1e-9 and lat_max - lat_min <= max_size + 1e-9
    ):
        return [",".join(str(x) for x in value)]
    lons = _edges(lon_min, lon_max, max_size)
    lats = _edges(lat_min, lat_max, max_size)
    limit = config.get_param("MAX_TILES")
    if len(lons) * len(lats) > limit:
        raise ValidationError(
            f"L'emprise in_bbox nécessiterait {len(lons) * len(lats)} tuiles de "
            f"{max_size}° (MAX_TILES = {limit}) : réduire l'emprise ou augmenter "
            "MAX_TILES."
        )
    return [f"{x0},{y0},{x1},{y1}" for y0, y1 in lats for x0, x1 in lons]


def bbox_param(value: Any, max_size: Optional[float]) -> str:
    """Valide une emprise qui doit tenir en une seule requête et la sérialise.

    Args:
        value: Liste ``[lon_min, lat_min, lon_max, lat_max]``.
        max_size: Largeur et hauteur maximales en degrés (``None`` : pas de limite).

    Returns:
        L'emprise au format ``"lon_min,lat_min,lon_max,lat_max"``.

    Raises:
        ValidationError: Si l'emprise est mal formée, inversée ou trop grande.
    """
    lon_min, lat_min, lon_max, lat_max = check_bbox(value)
    if max_size is not None and (
        lon_max - lon_min > max_size + 1e-9 or lat_max - lat_min > max_size + 1e-9
    ):
        raise ValidationError(
            f"L'emprise in_bbox ne doit pas excéder {max_size}° x {max_size}° "
            "pour cet endpoint."
        )
    return ",".join(str(x) for x in value)


def lon_lat_params(value: Any) -> Dict[str, str]:
    """Traduit un point en paramètres ``in_bbox`` et ``contains_geom``.

    Args:
        value: Liste ``[longitude, latitude]``.

    Returns:
        Les paramètres à transmettre à l'API.

    Raises:
        ValidationError: Si le point est mal formé ou hors bornes.
    """
    if (
        not isinstance(value, (list, tuple))
        or len(value) != 2
        or not all(is_num(x) for x in value)
    ):
        raise ValidationError("Le paramètre lon_lat doit être une liste de 2 floats.")
    lon, lat = value
    if not (-180 <= lon <= 180 and -90 <= lat <= 90):
        raise ValidationError("Le paramètre lon_lat sort des bornes géographiques.")
    half = LON_LAT_HALF_SIZE
    return {
        "in_bbox": f"{lon - half},{lat - half},{lon + half},{lat + half}",
        "contains_geom": json.dumps({"type": "Point", "coordinates": [lon, lat]}),
    }


def build_requests(
    endpoint: str,
    params: Dict[str, Any],
    *,
    path_code: bool = False,
    max_bbox: Optional[float] = BBOX_MAX_DEFAULT,
    location_required: bool = True,
) -> List[Tuple[str, Dict[str, Any]]]:
    """Traduit les paramètres d'un appel en liste de requêtes à exécuter.

    Args:
        endpoint: Chemin de l'endpoint, terminé par ``/``.
        params: Paramètres de l'appel (localisation comprise).
        path_code: ``True`` si le code géographique fait partie du chemin
            (``/indicateurs/.../<code>/``) plutôt que de la chaîne de requête.
        max_bbox: Taille maximale de l'emprise ``in_bbox`` en degrés ; une
            emprise plus grande est découpée en tuiles.
        location_required: ``False`` pour les endpoints sans localisation.

    Returns:
        La liste des couples ``(chemin, paramètres)`` à interroger.
    """
    params = dict(params)
    if not location_required and all(params.get(k) is None for k in LOCATION_KEYS):
        return [(endpoint, clean_params(params))]
    key, value = select_location(params)
    base = clean_params(params)

    if key == "lon_lat":
        return [(endpoint, {**base, **lon_lat_params(value)})]
    if key == "in_bbox":
        return [
            (endpoint, {**base, "in_bbox": tile}) for tile in tile_bbox(value, max_bbox)
        ]

    codes = as_list(value)
    if not codes:
        raise ValidationError(f"Le paramètre {key} ne peut pas être vide.")
    for code in codes:
        check_code(code, key)
    if path_code:
        return [(f"{endpoint}{quote(code, safe='')}/", dict(base)) for code in codes]
    if key == "coddep":
        return [(endpoint, {**base, key: code}) for code in codes]
    return [
        (endpoint, {**base, key: ",".join(group)})
        for group in chunks(codes, MAX_CODES_PER_REQUEST)
    ]


def _url(path: str) -> str:
    """Construit l'URL complète d'un chemin d'API.

    Args:
        path: Chemin commençant par ``/``, ou URL déjà absolue.

    Returns:
        L'URL absolue.
    """
    if path.startswith(("http://", "https://")):
        return path
    return f"{config.get_param('BASE_URL')}{path}"


def _collect_one(
    path: str,
    params: Dict[str, Any],
    *,
    use_token: bool,
    paginate: bool,
    progress: bool,
) -> List[Any]:
    """Exécute une requête et accumule les enregistrements de ses pages.

    Args:
        path: Chemin de l'endpoint (ou URL absolue).
        params: Paramètres de la requête.
        use_token: ``True`` pour les endpoints à accès restreint.
        paginate: ``True`` pour parcourir les pages suivantes.
        progress: ``True`` pour afficher une barre de progression par page.

    Returns:
        Les enregistrements (ou entités GeoJSON) de la requête.
    """
    records: List[Any] = []
    query = {"page_size": config.get_param("PAGE_SIZE"), **params}
    pbar: Optional[tqdm] = None
    try:
        for page, total in iter_pages(_url(path), query, use_token=use_token):
            records.extend(page)
            if progress and pbar is None and total:
                pbar = tqdm(total=total, desc=path, unit="enreg.")
            if pbar is not None:
                pbar.update(len(page))
            if not paginate:
                break
    finally:
        if pbar is not None:
            pbar.close()
    return records


def deduplicate(records: List[Any]) -> List[Any]:
    """Retire les enregistrements strictement identiques, en conservant l'ordre.

    Utile lorsque plusieurs requêtes (tuiles d'une emprise, notamment)
    renvoient le même objet.

    Args:
        records: Enregistrements ou entités GeoJSON.

    Returns:
        Les enregistrements sans doublon.
    """
    seen: set = set()
    unique: List[Any] = []
    for record in records:
        key = json.dumps(record, sort_keys=True, default=str)
        if key not in seen:
            seen.add(key)
            unique.append(record)
    return unique


def collect(
    requests_: Sequence[Tuple[str, Dict[str, Any]]],
    *,
    use_token: bool = False,
    paginate: bool = True,
) -> List[Any]:
    """Exécute les requêtes et accumule les enregistrements de toutes les pages.

    Plusieurs requêtes sont exécutées en parallèle (``MAX_WORKERS``), leurs
    résultats sont concaténés dans l'ordre du plan puis dédoublonnés.

    Args:
        requests_: Couples ``(chemin, paramètres)`` à interroger.
        use_token: ``True`` pour les endpoints à accès restreint.
        paginate: ``True`` pour parcourir les pages suivantes.

    Returns:
        La liste de tous les enregistrements (ou entités GeoJSON).
    """
    show = bool(config.get_param("PROGRESS_BAR"))
    if len(requests_) == 1:
        path, params = requests_[0]
        return _collect_one(
            path, params, use_token=use_token, paginate=paginate, progress=show
        )

    def run(item: Tuple[str, Dict[str, Any]]) -> List[Any]:
        return _collect_one(
            item[0], item[1], use_token=use_token, paginate=paginate, progress=False
        )

    workers = min(config.get_param("MAX_WORKERS"), len(requests_))
    results: List[List[Any]] = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        iterator: Iterable[List[Any]] = executor.map(run, requests_)
        if show:
            iterator = tqdm(
                iterator, total=len(requests_), desc=requests_[0][0], unit="requête"
            )
        results.extend(iterator)
    return deduplicate([record for result in results for record in result])


def to_table(records: List[Dict[str, Any]], output: Optional[str] = None) -> Any:
    """Assemble des enregistrements dans le format demandé.

    Args:
        records: Enregistrements renvoyés par l'API.
        output: ``"pandas"``, ``"polars"`` ou ``"dict"`` ; ``None`` pour
            appliquer ``OUTPUT_FORMAT``.

    Returns:
        Un ``pandas.DataFrame``, un ``polars.DataFrame`` ou la liste brute
        des enregistrements.

    Raises:
        ValidationError: Si le format n'est pas reconnu.
        ImportError: Si le format polars est demandé sans que polars soit installé.
    """
    fmt = output or config.get_param("OUTPUT_FORMAT")
    if fmt == "dict":
        return records
    if fmt == "polars":
        try:
            import polars as pl
        except ImportError as exc:  # pragma: no cover - dépend de l'environnement
            raise ImportError(
                "Le format polars nécessite le paquet polars : "
                "pip install 'apifoncier[polars]'."
            ) from exc
        return pl.DataFrame(records, infer_schema_length=None)
    if fmt == "pandas":
        return pd.DataFrame.from_records(records)
    raise ValidationError(
        f"output doit valoir 'pandas', 'polars' ou 'dict', reçu {output!r}."
    )


def to_geodataframe(features: List[Dict[str, Any]]) -> gpd.GeoDataFrame:
    """Assemble des entités GeoJSON en ``GeoDataFrame`` (EPSG:4326).

    L'identifiant de chaque entité, lorsqu'il est présent, sert d'index.

    Args:
        features: Entités GeoJSON renvoyées par l'API.

    Returns:
        Le ``GeoDataFrame`` correspondant, vide mais géoréférencé si aucune
        entité n'est renvoyée.
    """
    if not features:
        return gpd.GeoDataFrame(geometry=[], crs=CRS)
    gdf = gpd.GeoDataFrame.from_features(features, crs=CRS)
    ids = [feature.get("id") for feature in features]
    if all(identifier is not None for identifier in ids):
        gdf.index = pd.Index(ids)
    return gdf


def fetch(
    endpoint: str,
    params: Mapping[str, Any],
    *,
    use_token: bool = False,
    geo: bool = False,
    path_code: bool = False,
    max_bbox: Optional[float] = BBOX_MAX_DEFAULT,
    location_required: bool = True,
) -> Any:
    """Interroge un endpoint de liste et renvoie un tableau.

    Les clés ``paginate`` et ``output`` de ``params`` sont des options du
    module et ne sont pas transmises à l'API.

    Args:
        endpoint: Chemin de l'endpoint, terminé par ``/``.
        params: Paramètres de l'appel (les valeurs ``None`` sont ignorées).
        use_token: ``True`` pour les endpoints à accès restreint.
        geo: ``True`` pour un endpoint GeoJSON.
        path_code: ``True`` si le code géographique fait partie du chemin.
        max_bbox: Taille maximale d'une requête ``in_bbox`` en degrés.
        location_required: ``False`` pour les endpoints sans localisation.

    Returns:
        Pour un endpoint GeoJSON, un ``GeoDataFrame`` (ou une
        FeatureCollection si ``output="dict"``) ; sinon un tableau au format
        demandé.

    Raises:
        ValidationError: Si ``output`` n'est pas compatible avec l'endpoint.
    """
    params = dict(params)
    paginate = params.pop("paginate", True)
    output = params.pop("output", None)
    if paginate is None:
        paginate = True
    if geo and output not in (None, "pandas", "dict"):
        raise ValidationError(
            "Pour un endpoint géographique, output doit valoir 'pandas' "
            f"(GeoDataFrame) ou 'dict' (GeoJSON), reçu {output!r}."
        )
    plan = build_requests(
        endpoint,
        params,
        path_code=path_code,
        max_bbox=max_bbox,
        location_required=location_required,
    )
    records = collect(plan, use_token=use_token, paginate=bool(paginate))
    if geo:
        if output == "dict":
            return {"type": "FeatureCollection", "features": records}
        return to_geodataframe(records)
    return to_table(records, output)


def fetch_one(path: str, *, use_token: bool = False) -> Table:
    """Interroge un endpoint de détail et renvoie un tableau d'une ligne.

    Args:
        path: Chemin complet de la ressource (identifiant compris).
        use_token: ``True`` pour les endpoints à accès restreint.

    Returns:
        Un tableau d'une ligne au format défini par ``OUTPUT_FORMAT``.
    """
    payload = get_api_response(_url(path), use_token=use_token)
    return to_table([payload])

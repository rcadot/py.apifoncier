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


def bbox_param(value: Any, max_size: Optional[float]) -> str:
    """Valide une emprise rectangulaire et la sérialise.

    Args:
        value: Liste ``[lon_min, lat_min, lon_max, lat_max]``.
        max_size: Largeur et hauteur maximales en degrés (``None`` : pas de limite).

    Returns:
        L'emprise au format ``"lon_min,lat_min,lon_max,lat_max"``.

    Raises:
        ValidationError: Si l'emprise est mal formée, inversée ou trop grande.
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
        max_bbox: Taille maximale de l'emprise ``in_bbox`` en degrés.
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
        return [(endpoint, {**base, "in_bbox": bbox_param(value, max_bbox)})]

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


def collect(
    requests_: Sequence[Tuple[str, Dict[str, Any]]],
    *,
    use_token: bool = False,
    paginate: bool = True,
) -> List[Any]:
    """Exécute les requêtes et accumule les enregistrements de toutes les pages.

    Args:
        requests_: Couples ``(chemin, paramètres)`` à interroger.
        use_token: ``True`` pour les endpoints à accès restreint.
        paginate: ``True`` pour parcourir les pages suivantes.

    Returns:
        La liste de tous les enregistrements (ou entités GeoJSON).
    """
    records: List[Any] = []
    show = bool(config.get_param("PROGRESS_BAR"))
    page_size = config.get_param("PAGE_SIZE")
    for path, params in requests_:
        query = {"page_size": page_size, **params}
        pbar: Optional[tqdm] = None
        try:
            for page, total in iter_pages(_url(path), query, use_token=use_token):
                records.extend(page)
                if show and pbar is None and total:
                    pbar = tqdm(total=total, desc=path, unit="enreg.")
                if pbar is not None:
                    pbar.update(len(page))
                if not paginate:
                    break
        finally:
            if pbar is not None:
                pbar.close()
    return records


def to_table(records: List[Dict[str, Any]]) -> Table:
    """Assemble des enregistrements en tableau selon ``OUTPUT_FORMAT``.

    Args:
        records: Enregistrements renvoyés par l'API.

    Returns:
        Un ``pandas.DataFrame`` ou un ``polars.DataFrame``.

    Raises:
        ImportError: Si le format polars est demandé sans que polars soit installé.
    """
    if config.get_param("OUTPUT_FORMAT") == "polars":
        try:
            import polars as pl
        except ImportError as exc:  # pragma: no cover - dépend de l'environnement
            raise ImportError(
                "Le format polars nécessite le paquet polars : "
                "pip install 'apifoncier[polars]'."
            ) from exc
        return pl.DataFrame(records, infer_schema_length=None)
    return pd.DataFrame.from_records(records)


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
) -> Union[Table, gpd.GeoDataFrame]:
    """Interroge un endpoint de liste et renvoie un tableau.

    Args:
        endpoint: Chemin de l'endpoint, terminé par ``/``.
        params: Paramètres de l'appel (les valeurs ``None`` sont ignorées).
        use_token: ``True`` pour les endpoints à accès restreint.
        geo: ``True`` pour un endpoint GeoJSON.
        path_code: ``True`` si le code géographique fait partie du chemin.
        max_bbox: Taille maximale de l'emprise ``in_bbox`` en degrés.
        location_required: ``False`` pour les endpoints sans localisation.

    Returns:
        Un ``GeoDataFrame`` si ``geo`` est vrai, sinon un tableau au format
        défini par ``OUTPUT_FORMAT``.
    """
    plan = build_requests(
        endpoint,
        dict(params),
        path_code=path_code,
        max_bbox=max_bbox,
        location_required=location_required,
    )
    records = collect(plan, use_token=use_token)
    return to_geodataframe(records) if geo else to_table(records)


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

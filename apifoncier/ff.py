"""Fichiers fonciers : parcelles, TUP, locaux et droits de propriété.

Accès restreint : un jeton est requis (voir :func:`apifoncier.configure`).

Endpoints interrogés :

* ``/ff/parcelles/`` et ``/ff/geoparcelles/`` ; ``/ff/parcelles/<idpar>/`` ;
* ``/ff/tups/`` et ``/ff/geotups/`` ; ``/ff/tups/<idtup>/`` ;
* ``/ff/locaux/`` ; ``/ff/locaux/<idlocal>/`` ;
* ``/ff/proprios/`` ; ``/ff/proprios/<idprodroit>/``.
"""

from __future__ import annotations

import warnings
from typing import Any, Dict, Optional

import geopandas as gpd

from ._query import BBox, Codes, Multi, Point, Table, fetch, fetch_one, path_segment

_DEPRECATED_PARAMS = {
    "jannathmin_min": "jannatmin_min",
    "jannathmin_max": "jannatmin_max",
}


def _rename_deprecated(params: Dict[str, Any]) -> None:
    """Remplace les noms de paramètres obsolètes par leur nom correct.

    Les versions antérieures exposaient ``jannathmin_min`` et ``jannathmin_max``,
    noms que l'API ne reconnaît pas : le filtre était silencieusement ignoré.

    Args:
        params: Paramètres de l'appel, modifiés sur place.
    """
    for old, new in _DEPRECATED_PARAMS.items():
        value = params.pop(old, None)
        if value is None:
            continue
        warnings.warn(
            f"Le paramètre {old} est obsolète, utiliser {new}.",
            DeprecationWarning,
            stacklevel=3,
        )
        if params.get(new) is None:
            params[new] = value


########################################################################
# PARCELLES
########################################################################


def parcelles(
    code_insee: Codes = None,
    in_bbox: BBox = None,
    lon_lat: Point = None,
    fields: Optional[str] = None,
    ordering: Optional[str] = None,
    catpro3: Multi = None,
    ctpdl: Optional[str] = None,
    dcntarti_min: Optional[float] = None,
    dcntarti_max: Optional[float] = None,
    dcntnaf_min: Optional[float] = None,
    dcntnaf_max: Optional[float] = None,
    dcntpa_min: Optional[float] = None,
    dcntpa_max: Optional[float] = None,
    idcomtxt: Optional[str] = None,
    idpar: Multi = None,
    jannatmin_min: Optional[int] = None,
    jannatmin_max: Optional[int] = None,
    nlocal_min: Optional[int] = None,
    nlocal_max: Optional[int] = None,
    nlogh_min: Optional[int] = None,
    nlogh_max: Optional[int] = None,
    slocal_min: Optional[float] = None,
    slocal_max: Optional[float] = None,
    sprincp_min: Optional[float] = None,
    sprincp_max: Optional[float] = None,
    stoth_min: Optional[float] = None,
    stoth_max: Optional[float] = None,
    jannathmin_min: Optional[int] = None,
    jannathmin_max: Optional[int] = None,
) -> Table:
    """Retourne les parcelles issues des Fichiers fonciers pour le périmètre demandé.

    Un paramètre de localisation au moins est requis : ``code_insee``,
    ``in_bbox`` ou ``lon_lat``.

    Args:
        code_insee: Code(s) INSEE communaux ou d'arrondissements municipaux.
        in_bbox: Emprise ``[lon_min, lat_min, lon_max, lat_max]``,
            0,02° x 0,02° au plus.
        lon_lat: Point ``[longitude, latitude]`` contenu dans les parcelles renvoyées.
        fields: ``"all"`` pour obtenir tous les champs.
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        catpro3: Code(s) de catégorie de propriétaire ; les premiers niveaux suffisent.
        ctpdl: Type de propriété divisée en lots (type de copropriété).
        dcntarti_min: Surface artificialisée minimale de la parcelle (m²).
        dcntarti_max: Surface artificialisée maximale de la parcelle (m²).
        dcntnaf_min: Surface NAF minimale de la parcelle (m²).
        dcntnaf_max: Surface NAF maximale de la parcelle (m²).
        dcntpa_min: Surface minimale de la parcelle (m²).
        dcntpa_max: Surface maximale de la parcelle (m²).
        idcomtxt: Chaîne contenue dans le libellé de la commune.
        idpar: Identifiant(s) de parcelle (liste ou chaîne séparée par des virgules).
        jannatmin_min: Année minimale de construction du local le plus ancien.
        jannatmin_max: Année maximale de construction du local le plus ancien.
        nlocal_min: Nombre minimal de locaux sur la parcelle.
        nlocal_max: Nombre maximal de locaux sur la parcelle.
        nlogh_min: Nombre minimal de logements sur la parcelle.
        nlogh_max: Nombre maximal de logements sur la parcelle.
        slocal_min: Surface minimale des parties d'évaluation (m²).
        slocal_max: Surface maximale des parties d'évaluation (m²).
        sprincp_min: Surface minimale des pièces principales professionnelles (m²).
        sprincp_max: Surface maximale des pièces principales professionnelles (m²).
        stoth_min: Surface minimale des pièces d'habitation (m²).
        stoth_max: Surface maximale des pièces d'habitation (m²).
        jannathmin_min: Obsolète, remplacé par ``jannatmin_min``.
        jannathmin_max: Obsolète, remplacé par ``jannatmin_max``.

    Returns:
        Un tableau des parcelles (``pandas`` ou ``polars`` selon ``OUTPUT_FORMAT``).

    Examples:
        >>> import apifoncier.ff as ff
        >>> ff.parcelles(code_insee="59350", dcntpa_min=3000)
        >>> ff.parcelles(in_bbox=[3, 50, 3.01, 50.01])
    """
    params = dict(locals())
    _rename_deprecated(params)
    return fetch("/ff/parcelles/", params, use_token=True)


def geoparcelles(
    code_insee: Codes = None,
    in_bbox: BBox = None,
    lon_lat: Point = None,
    fields: Optional[str] = None,
    ordering: Optional[str] = None,
    catpro3: Multi = None,
    ctpdl: Optional[str] = None,
    dcntarti_min: Optional[float] = None,
    dcntarti_max: Optional[float] = None,
    dcntnaf_min: Optional[float] = None,
    dcntnaf_max: Optional[float] = None,
    dcntpa_min: Optional[float] = None,
    dcntpa_max: Optional[float] = None,
    idcomtxt: Optional[str] = None,
    idpar: Multi = None,
    jannatmin_min: Optional[int] = None,
    jannatmin_max: Optional[int] = None,
    nlocal_min: Optional[int] = None,
    nlocal_max: Optional[int] = None,
    nlogh_min: Optional[int] = None,
    nlogh_max: Optional[int] = None,
    slocal_min: Optional[float] = None,
    slocal_max: Optional[float] = None,
    sprincp_min: Optional[float] = None,
    sprincp_max: Optional[float] = None,
    stoth_min: Optional[float] = None,
    stoth_max: Optional[float] = None,
    jannathmin_min: Optional[int] = None,
    jannathmin_max: Optional[int] = None,
) -> gpd.GeoDataFrame:
    """Retourne les parcelles issues des Fichiers fonciers avec leurs contours.

    Un paramètre de localisation au moins est requis : ``code_insee``,
    ``in_bbox`` ou ``lon_lat``.

    Args:
        code_insee: Code(s) INSEE communaux ou d'arrondissements municipaux.
        in_bbox: Emprise ``[lon_min, lat_min, lon_max, lat_max]``,
            0,02° x 0,02° au plus.
        lon_lat: Point ``[longitude, latitude]`` contenu dans les parcelles renvoyées.
        fields: ``"all"`` pour obtenir tous les champs.
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        catpro3: Code(s) de catégorie de propriétaire ; les premiers niveaux suffisent.
        ctpdl: Type de propriété divisée en lots (type de copropriété).
        dcntarti_min: Surface artificialisée minimale de la parcelle (m²).
        dcntarti_max: Surface artificialisée maximale de la parcelle (m²).
        dcntnaf_min: Surface NAF minimale de la parcelle (m²).
        dcntnaf_max: Surface NAF maximale de la parcelle (m²).
        dcntpa_min: Surface minimale de la parcelle (m²).
        dcntpa_max: Surface maximale de la parcelle (m²).
        idcomtxt: Chaîne contenue dans le libellé de la commune.
        idpar: Identifiant(s) de parcelle (liste ou chaîne séparée par des virgules).
        jannatmin_min: Année minimale de construction du local le plus ancien.
        jannatmin_max: Année maximale de construction du local le plus ancien.
        nlocal_min: Nombre minimal de locaux sur la parcelle.
        nlocal_max: Nombre maximal de locaux sur la parcelle.
        nlogh_min: Nombre minimal de logements sur la parcelle.
        nlogh_max: Nombre maximal de logements sur la parcelle.
        slocal_min: Surface minimale des parties d'évaluation (m²).
        slocal_max: Surface maximale des parties d'évaluation (m²).
        sprincp_min: Surface minimale des pièces principales professionnelles (m²).
        sprincp_max: Surface maximale des pièces principales professionnelles (m²).
        stoth_min: Surface minimale des pièces d'habitation (m²).
        stoth_max: Surface maximale des pièces d'habitation (m²).
        jannathmin_min: Obsolète, remplacé par ``jannatmin_min``.
        jannathmin_max: Obsolète, remplacé par ``jannatmin_max``.

    Returns:
        Un ``GeoDataFrame`` (EPSG:4326) indexé par l'identifiant des parcelles.

    Examples:
        >>> import apifoncier.ff as ff
        >>> ff.geoparcelles(code_insee="59350", dcntpa_min=3000)
        >>> ff.geoparcelles(lon_lat=[3.06, 50.63])
    """
    params = dict(locals())
    _rename_deprecated(params)
    return fetch("/ff/geoparcelles/", params, geo=True, use_token=True)


def parcelle(idpar: str) -> Table:
    """Retourne la parcelle correspondant à l'identifiant ``idpar``.

    Args:
        idpar: Identifiant de la parcelle.

    Returns:
        Un tableau d'une ligne.

    Raises:
        ValidationError: Si l'identifiant est absent ou invalide.
    """
    return fetch_one(f"/ff/parcelles/{path_segment(idpar, 'idpar')}/", use_token=True)


########################################################################
# TUPS
########################################################################


def tups(
    code_insee: Codes = None,
    in_bbox: BBox = None,
    lon_lat: Point = None,
    fields: Optional[str] = None,
    ordering: Optional[str] = None,
    catpro3: Multi = None,
    idtup: Multi = None,
    typetup: Optional[str] = None,
) -> Table:
    """Retourne les unités foncières (TUP) issues des Fichiers fonciers.

    Un paramètre de localisation au moins est requis : ``code_insee``,
    ``in_bbox`` ou ``lon_lat``.

    Args:
        code_insee: Code(s) INSEE communaux ou d'arrondissements municipaux.
        in_bbox: Emprise ``[lon_min, lat_min, lon_max, lat_max]``,
            0,02° x 0,02° au plus.
        lon_lat: Point ``[longitude, latitude]`` contenu dans les TUP renvoyées.
        fields: ``"all"`` pour obtenir tous les champs.
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        catpro3: Code(s) de catégorie de propriétaire ; les premiers niveaux suffisent.
        idtup: Identifiant(s) de TUP (liste ou chaîne séparée par des virgules).
        typetup: Type de TUP (``SIMPLE``, ``PDLMP`` ou ``UF``).

    Returns:
        Un tableau des TUP (``pandas`` ou ``polars`` selon ``OUTPUT_FORMAT``).

    Examples:
        >>> import apifoncier.ff as ff
        >>> ff.tups(code_insee="59350", catpro3="P")
        >>> ff.tups(in_bbox=[3, 50, 3.01, 50.01])
    """
    params = dict(locals())
    return fetch("/ff/tups/", params, use_token=True)


def geotups(
    code_insee: Codes = None,
    in_bbox: BBox = None,
    lon_lat: Point = None,
    fields: Optional[str] = None,
    ordering: Optional[str] = None,
    catpro3: Multi = None,
    idtup: Multi = None,
    typetup: Optional[str] = None,
) -> gpd.GeoDataFrame:
    """Retourne les unités foncières (TUP) issues des Fichiers fonciers avec leurs contours.

    Un paramètre de localisation au moins est requis : ``code_insee``,
    ``in_bbox`` ou ``lon_lat``.

    Args:
        code_insee: Code(s) INSEE communaux ou d'arrondissements municipaux.
        in_bbox: Emprise ``[lon_min, lat_min, lon_max, lat_max]``,
            0,02° x 0,02° au plus.
        lon_lat: Point ``[longitude, latitude]`` contenu dans les TUP renvoyées.
        fields: ``"all"`` pour obtenir tous les champs.
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        catpro3: Code(s) de catégorie de propriétaire ; les premiers niveaux suffisent.
        idtup: Identifiant(s) de TUP (liste ou chaîne séparée par des virgules).
        typetup: Type de TUP (``SIMPLE``, ``PDLMP`` ou ``UF``).

    Returns:
        Un ``GeoDataFrame`` (EPSG:4326) indexé par l'identifiant des TUP.

    Examples:
        >>> import apifoncier.ff as ff
        >>> ff.geotups(code_insee="59350", catpro3="P")
        >>> ff.geotups(in_bbox=[3, 50, 3.01, 50.01])
    """
    params = dict(locals())
    return fetch("/ff/geotups/", params, geo=True, use_token=True)


def tup(idtup: str) -> Table:
    """Retourne la TUP correspondant à l'identifiant ``idtup``.

    Args:
        idtup: Identifiant de la TUP.

    Returns:
        Un tableau d'une ligne.

    Raises:
        ValidationError: Si l'identifiant est absent ou invalide.
    """
    return fetch_one(f"/ff/tups/{path_segment(idtup, 'idtup')}/", use_token=True)


########################################################################
# LOCAUX
########################################################################


def locaux(
    code_insee: Codes = None,
    fields: Optional[str] = None,
    ordering: Optional[str] = None,
    catpro3: Multi = None,
    dteloc: Multi = None,
    idpar: Optional[str] = None,
    idprocpte: Optional[str] = None,
    idsec: Optional[str] = None,
    locprop: Multi = None,
    loghlls: Optional[str] = None,
    proba_rprs: Multi = None,
    slocal_min: Optional[float] = None,
    slocal_max: Optional[float] = None,
    typeact: Multi = None,
) -> Table:
    """Retourne les locaux issus des Fichiers fonciers pour les communes demandées.

    Args:
        code_insee: Code(s) INSEE communaux ou d'arrondissements municipaux (requis).
        fields: ``"all"`` pour obtenir tous les champs.
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        catpro3: Code(s) de catégorie de propriétaire ; les premiers niveaux suffisent.
        dteloc: Type(s) de local.
        idpar: Identifiant de parcelle.
        idprocpte: Identifiant de compte communal.
        idsec: Identifiant de section cadastrale.
        locprop: Localisation(s) généralisée(s) du propriétaire.
        loghlls: Logement social repéré par exonération.
        proba_rprs: Probabilité(s) de résidence principale ou secondaire.
        slocal_min: Surface minimale des parties d'évaluation (m²).
        slocal_max: Surface maximale des parties d'évaluation (m²).
        typeact: Code(s) de catégorie de local d'activité ; les premiers niveaux suffisent.

    Returns:
        Un tableau des locaux (``pandas`` ou ``polars`` selon ``OUTPUT_FORMAT``).

    Examples:
        >>> import apifoncier.ff as ff
        >>> ff.locaux(code_insee="59350", dteloc=["1", "2"])
    """
    params = dict(locals())
    return fetch("/ff/locaux/", params, use_token=True)


def local(idlocal: str) -> Table:
    """Retourne le local correspondant à l'identifiant ``idlocal``.

    Args:
        idlocal: Identifiant fiscal du local.

    Returns:
        Un tableau d'une ligne.

    Raises:
        ValidationError: Si l'identifiant est absent ou invalide.
    """
    return fetch_one(f"/ff/locaux/{path_segment(idlocal, 'idlocal')}/", use_token=True)


########################################################################
# PROPRIOS
########################################################################


def proprios(
    code_insee: Codes = None,
    fields: Optional[str] = None,
    ordering: Optional[str] = None,
    catpro3: Multi = None,
    ccodro: Multi = None,
    gtoper: Optional[str] = None,
    idprocpte: Optional[str] = None,
    locprop: Multi = None,
    typedroit: Optional[str] = None,
) -> Table:
    """Retourne les droits de propriété issus des Fichiers fonciers.

    Args:
        code_insee: Code(s) INSEE communaux ou d'arrondissements municipaux (requis).
        fields: ``"all"`` pour obtenir tous les champs.
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        catpro3: Code(s) de catégorie de propriétaire ; les premiers niveaux suffisent.
        ccodro: Code(s) du droit réel ou particulier.
        gtoper: Indicateur de personne physique ou morale.
        idprocpte: Identifiant de compte communal.
        locprop: Localisation(s) généralisée(s) du propriétaire.
        typedroit: Type de droit : propriétaire ou gestionnaire.

    Returns:
        Un tableau des droits de propriété (``pandas`` ou ``polars``).

    Examples:
        >>> import apifoncier.ff as ff
        >>> ff.proprios(code_insee="59350")
    """
    params = dict(locals())
    return fetch("/ff/proprios/", params, use_token=True)


def proprio(idprodroit: str) -> Table:
    """Retourne le droit de propriété correspondant à l'identifiant ``idprodroit``.

    Args:
        idprodroit: Identifiant du droit de propriété.

    Returns:
        Un tableau d'une ligne.

    Raises:
        ValidationError: Si l'identifiant est absent ou invalide.
    """
    return fetch_one(
        f"/ff/proprios/{path_segment(idprodroit, 'idprodroit')}/", use_token=True
    )

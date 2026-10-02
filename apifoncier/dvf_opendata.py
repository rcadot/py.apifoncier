"""Mutations issues de DVF+ open data (accès libre).

Endpoints interrogés :

* ``/dvf_opendata/mutations/`` : liste des mutations ;
* ``/dvf_opendata/geomutations/`` : liste des mutations au format GeoJSON ;
* ``/dvf_opendata/mutations/<idmutation>/`` : détail d'une mutation.
"""

from __future__ import annotations

from typing import Optional, Union

import geopandas as gpd

from ._query import BBox, Codes, Multi, Point, Table, fetch, fetch_one, path_segment


def mutations(
    code_insee: Codes = None,
    in_bbox: BBox = None,
    lon_lat: Point = None,
    fields: Optional[str] = None,
    ordering: Optional[str] = None,
    anneemut_min: Optional[Union[int, str]] = None,
    anneemut_max: Optional[Union[int, str]] = None,
    anneemut: Optional[Union[int, str]] = None,
    codtypbien: Multi = None,
    idnatmut: Multi = None,
    sbati_min: Optional[float] = None,
    sbati_max: Optional[float] = None,
    sterr_min: Optional[float] = None,
    sterr_max: Optional[float] = None,
    valeurfonc_min: Optional[float] = None,
    valeurfonc_max: Optional[float] = None,
    vefa: Optional[Union[bool, str]] = None,
    segmtab: Multi = None,
    paginate: bool = True,
    output: Optional[str] = None,
) -> Table:
    """Retourne les mutations issues de DVF+ open data pour le périmètre demandé.

    Un paramètre de localisation au moins est requis : ``code_insee``,
    ``in_bbox`` ou ``lon_lat``.

    Args:
        code_insee: Code(s) INSEE communaux ou d'arrondissements municipaux.
        in_bbox: Emprise ``[lon_min, lat_min, lon_max, lat_max]``,
            0,02° x 0,02° au plus.
        lon_lat: Point ``[longitude, latitude]`` contenu dans les mutations renvoyées.
        fields: ``"all"`` pour obtenir tous les champs.
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        anneemut_min: Année de mutation minimale.
        anneemut_max: Année de mutation maximale.
        anneemut: Année de mutation.
        codtypbien: Code(s) de typologie de bien ; les premiers niveaux suffisent
            (liste ou chaîne séparée par des virgules).
        idnatmut: Code(s) de nature de mutation (liste ou chaîne séparée par des virgules).
        sbati_min: Surface bâtie minimale (m²).
        sbati_max: Surface bâtie maximale (m²).
        sterr_min: Surface de terrain minimale (m²).
        sterr_max: Surface de terrain maximale (m²).
        valeurfonc_min: Valeur foncière minimale (€).
        valeurfonc_max: Valeur foncière maximale (€).
        vefa: Vente en l'état futur d'achèvement.
        segmtab: Note(s) de segment du terrain à bâtir.
        paginate: ``False`` pour ne récupérer que la première page.
        output: ``"pandas"``, ``"polars"`` ou ``"dict"`` ; par défaut ``OUTPUT_FORMAT``.

    Returns:
        Un tableau des mutations (``pandas`` ou ``polars`` selon ``OUTPUT_FORMAT``).

    Examples:
        >>> import apifoncier.dvf_opendata as dvf
        >>> dvf.mutations(code_insee="59001")
        >>> dvf.mutations(in_bbox=[3, 50, 3.01, 50.01], fields="all")
        >>> dvf.mutations(code_insee=["59350", "59646"], valeurfonc_min=1000000)
    """
    params = dict(locals())
    return fetch("/dvf_opendata/mutations/", params)


def geomutations(
    code_insee: Codes = None,
    in_bbox: BBox = None,
    lon_lat: Point = None,
    fields: Optional[str] = None,
    ordering: Optional[str] = None,
    anneemut_min: Optional[Union[int, str]] = None,
    anneemut_max: Optional[Union[int, str]] = None,
    anneemut: Optional[Union[int, str]] = None,
    codtypbien: Multi = None,
    idnatmut: Multi = None,
    sbati_min: Optional[float] = None,
    sbati_max: Optional[float] = None,
    sterr_min: Optional[float] = None,
    sterr_max: Optional[float] = None,
    valeurfonc_min: Optional[float] = None,
    valeurfonc_max: Optional[float] = None,
    vefa: Optional[Union[bool, str]] = None,
    segmtab: Multi = None,
    paginate: bool = True,
    output: Optional[str] = None,
) -> gpd.GeoDataFrame:
    """Retourne les mutations issues de DVF+ open data avec leurs géométries.

    Un paramètre de localisation au moins est requis : ``code_insee``,
    ``in_bbox`` ou ``lon_lat``.

    Args:
        code_insee: Code(s) INSEE communaux ou d'arrondissements municipaux.
        in_bbox: Emprise ``[lon_min, lat_min, lon_max, lat_max]``,
            0,02° x 0,02° au plus.
        lon_lat: Point ``[longitude, latitude]`` contenu dans les mutations renvoyées.
        fields: ``"all"`` pour obtenir tous les champs.
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        anneemut_min: Année de mutation minimale.
        anneemut_max: Année de mutation maximale.
        anneemut: Année de mutation.
        codtypbien: Code(s) de typologie de bien ; les premiers niveaux suffisent
            (liste ou chaîne séparée par des virgules).
        idnatmut: Code(s) de nature de mutation (liste ou chaîne séparée par des virgules).
        sbati_min: Surface bâtie minimale (m²).
        sbati_max: Surface bâtie maximale (m²).
        sterr_min: Surface de terrain minimale (m²).
        sterr_max: Surface de terrain maximale (m²).
        valeurfonc_min: Valeur foncière minimale (€).
        valeurfonc_max: Valeur foncière maximale (€).
        vefa: Vente en l'état futur d'achèvement.
        segmtab: Note(s) de segment du terrain à bâtir.
        paginate: ``False`` pour ne récupérer que la première page.
        output: ``"dict"`` pour obtenir une FeatureCollection GeoJSON plutôt
            qu'un ``GeoDataFrame``.

    Returns:
        Un ``GeoDataFrame`` (EPSG:4326) indexé par l'identifiant des mutations.

    Examples:
        >>> import apifoncier.dvf_opendata as dvf
        >>> dvf.geomutations(code_insee="59001")
        >>> dvf.geomutations(in_bbox=[3, 50, 3.01, 50.01], fields="all")
    """
    params = dict(locals())
    return fetch("/dvf_opendata/geomutations/", params, geo=True)


def mutation(idmutation: Union[int, str]) -> Table:
    """Retourne la mutation correspondant à l'identifiant ``idmutation``.

    Args:
        idmutation: Identifiant de la mutation.

    Returns:
        Un tableau d'une ligne décrivant la mutation.

    Raises:
        ValidationError: Si l'identifiant est absent ou invalide.
    """
    return fetch_one(
        f"/dvf_opendata/mutations/{path_segment(idmutation, 'idmutation')}/"
    )

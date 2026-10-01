"""Friches issues de Cartofriches (accès libre).

Endpoints interrogés :

* ``/cartofriches/friches/`` : liste des friches ;
* ``/cartofriches/geofriches/`` : liste des friches au format GeoJSON ;
* ``/cartofriches/friches/<site_id>/`` : détail d'une friche.
"""

from __future__ import annotations

from typing import Optional

import geopandas as gpd

from ._query import (
    BBOX_MAX_CARTOFRICHES,
    BBox,
    Codes,
    Point,
    Table,
    fetch,
    fetch_one,
    path_segment,
)


def friches(
    code_insee: Codes = None,
    coddep: Codes = None,
    in_bbox: BBox = None,
    lon_lat: Point = None,
    fields: Optional[str] = None,
    ordering: Optional[str] = None,
    surface_max: Optional[float] = None,
    surface_min: Optional[float] = None,
    urba_zone_type: Optional[str] = None,
) -> Table:
    """Retourne les friches issues de Cartofriches pour le périmètre demandé.

    Un paramètre de localisation au moins est requis : ``code_insee``,
    ``coddep``, ``in_bbox`` ou ``lon_lat``.

    Args:
        code_insee: Code(s) INSEE communaux ou d'arrondissements municipaux.
        coddep: Code(s) INSEE des départements.
        in_bbox: Emprise ``[lon_min, lat_min, lon_max, lat_max]``, 1° x 1° au plus.
        lon_lat: Point ``[longitude, latitude]`` contenu dans les friches renvoyées.
        fields: ``"all"`` pour obtenir tous les champs.
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        surface_max: Surface maximale de l'unité foncière (m²).
        surface_min: Surface minimale de l'unité foncière (m²).
        urba_zone_type: Type de zone d'urbanisme.

    Returns:
        Un tableau des friches (``pandas`` ou ``polars`` selon ``OUTPUT_FORMAT``).

    Examples:
        >>> import apifoncier.cartofriches as cartofriches
        >>> cartofriches.friches(code_insee="59350")
        >>> cartofriches.friches(coddep="59", surface_min=10000)
        >>> cartofriches.friches(in_bbox=[3, 50, 4, 51])
    """
    params = dict(locals())
    return fetch("/cartofriches/friches/", params, max_bbox=BBOX_MAX_CARTOFRICHES)


def geofriches(
    code_insee: Codes = None,
    coddep: Codes = None,
    in_bbox: BBox = None,
    lon_lat: Point = None,
    fields: Optional[str] = None,
    ordering: Optional[str] = None,
    surface_max: Optional[float] = None,
    surface_min: Optional[float] = None,
    urba_zone_type: Optional[str] = None,
) -> gpd.GeoDataFrame:
    """Retourne les friches issues de Cartofriches avec leurs contours.

    Un paramètre de localisation au moins est requis : ``code_insee``,
    ``coddep``, ``in_bbox`` ou ``lon_lat``.

    Args:
        code_insee: Code(s) INSEE communaux ou d'arrondissements municipaux.
        coddep: Code(s) INSEE des départements.
        in_bbox: Emprise ``[lon_min, lat_min, lon_max, lat_max]``, 1° x 1° au plus.
        lon_lat: Point ``[longitude, latitude]`` contenu dans les friches renvoyées.
        fields: ``"all"`` pour obtenir tous les champs.
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        surface_max: Surface maximale de l'unité foncière (m²).
        surface_min: Surface minimale de l'unité foncière (m²).
        urba_zone_type: Type de zone d'urbanisme.

    Returns:
        Un ``GeoDataFrame`` (EPSG:4326) indexé par l'identifiant des friches.

    Examples:
        >>> import apifoncier.cartofriches as cartofriches
        >>> cartofriches.geofriches(code_insee="59350")
        >>> cartofriches.geofriches(coddep="59")
        >>> cartofriches.geofriches(in_bbox=[3, 50, 4, 51])
    """
    params = dict(locals())
    return fetch(
        "/cartofriches/geofriches/", params, geo=True, max_bbox=BBOX_MAX_CARTOFRICHES
    )


def friche(site_id: str) -> Table:
    """Retourne la friche correspondant à l'identifiant ``site_id``.

    Args:
        site_id: Identifiant du site Cartofriches.

    Returns:
        Un tableau d'une ligne décrivant la friche.

    Raises:
        ValidationError: Si l'identifiant est absent ou invalide.
    """
    return fetch_one(f"/cartofriches/friches/{path_segment(site_id, 'site_id')}/")

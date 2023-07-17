import pandas as pd
from .config import get_param

from . import utils


def friches(
    code_insee=None,
    coddep=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
    surface_max=None,
    surface_min=None,
    urba_zone_type=None,
):
    """Retourne les friches issues de Cartofriches pour le périmètre demandé sous forme d'un dataframe

    Args:
        **code_insee (str or list, optional)**: Codes INSEE communaux ou des arrondissements municipaux. Defaults to None.
        **coddep (str or list, optional)**: Codes INSEE des départements. Defaults to None.
        **in_bbox (list, optional)**: Emprise rectangulaire sous la forme d'une liste [longitude_min, latitude_min, longitude_min, latitude_max]. Defaults to None.
        **lon_lat (list, optional)**: Coordonnée du point au sein de la ou des friches renvoyées [longitude, latitude]. Defaults to None.
        **fields (str, optional)**: Mettre à "all" pour obtenir tous les champs associés. Defaults to None.
        **ordering (str, optional)**: Champs à utiliser pour ordonner le résultat. Defaults to None.
        **surface_max (int, optional)**: Surface maximale des friches. Defaults to None.
        **surface_min (int, optional)**: Surface minimale des friches. Defaults to None.
        **urba_zone_type (str, optional)**: Type de zonage. Defaults to None.

    Returns:
        dataframe: données sur les friches issues de Cartofriches
    """
    result = utils.Resultat("/cartofriches/friches/", **locals())
    df = result.get_dataframe()
    return df


def geofriches(
    code_insee=None,
    coddep=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
    surface_max=None,
    surface_min=None,
    urba_zone_type=None,
):
    """Retourne les friches issues de Cartofriches pour le périmètre demandé sous forme d'un geodataframe

    Args:
        **code_insee (str or list, optional)**: Codes INSEE communaux ou des arrondissements municipaux. Defaults to None.
        **coddep (str or list, optional)**: Codes INSEE des départements. Defaults to None.
        **in_bbox (list, optional)**: Emprise rectangulaire sous la forme d'une liste [longitude_min, latitude_min, longitude_min, latitude_max]. Defaults to None.
        **lon_lat (list, optional)**: Coordonnée du point au sein de la ou des friches renvoyées [longitude, latitude]. Defaults to None.
        **fields (str, optional)**: Mettre à "all" pour obtenir tous les champs associés. Defaults to None.
        **ordering (str, optional)**: Champs à utiliser pour ordonner le résultat. Defaults to None.
        **surface_max (int, optional)**: Surface maximale des friches. Defaults to None.
        **surface_min (int, optional)**: Surface minimale des friches. Defaults to None.
        **urba_zone_type (str, optional)**: Type de zonage. Defaults to None.

    Returns:
        geodataframe: données sur les friches issues de Cartofriches avec les contours géométriques
    """
    result = utils.Resultat("/cartofriches/geofriches/", **locals())
    gdf = result.get_geodataframe()
    return gdf


def friche(site_id=None):
    """Renvoi la friche correpondant au site_id (str)

    Returns:
        dataframe: donnée sur la friche issue de Cartofriches
    """

    base_url = get_param("BASE_URL")
    url = f"""{base_url}/cartofriches/friches/{site_id}/"""
    response = utils.get_api_response(url)
    return pd.DataFrame.from_dict(response)

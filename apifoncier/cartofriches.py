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
    """Retourne les friches issues de Cartofriches pour la commune demandée

    Args:
        code_insee (str): Code INSEE communal ou d'arrondissement municipal (possibilité de passer une liste de code insee sans limite maximum)

        TODO

        fields (str, optional): Retourne tous les champs associés si fields=all, sinon retourne uniquement une selection de champs. Defaults to None.

        ordering (str, optional): Which field to use when ordering the results. Defaults to None.

        surface_max (int, optional): Surface maximale de l'unité foncière. Defaults to None.

        surface_min (int, optional): Surface minimale de l'unité foncière. Defaults to None.

        urba_zone_type (str, optional): Type de zone d'urbanisme. Defaults to None.

    Returns:
        dataframe: Retourne les friches issues de Cartofriches pour la commune demandée

    >>> apifoncier.cartofriches.friches([59350,59002])
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
    """Retourne les friches issues de Cartofriches pour la commune demandée sous forme d'un geodataframe

    Args:
        code_insee (str): Code INSEE communal ou d'arrondissement municipal (possibilité de passer une liste de code insee sans limite maximum)

        **fields (str, optional):** Retourne tous les champs associés si fields=all, sinon retourne uniquement une selection de champs. Defaults to None.

        ordering (str, optional): Which field to use when ordering the results. Defaults to None.

        surface_max (int, optional): Surface maximale de l'unité foncière. Defaults to None.

        surface_min (int, optional): Surface minimale de l'unité foncière. Defaults to None.

        urba_zone_type (str, optional): Type de zone d'urbanisme. Defaults to None.

    Returns:
        dataframe: Retourne les friches issues de Cartofriches pour la commune demandée

    >>> apifoncier.cartofriches.friches(code_insee=[59350,59002])
    """
    result = utils.Resultat("/cartofriches/geofriches/", **locals())
    gdf = result.get_geodataframe()
    return gdf


def friche(site_id=None):
    base_url = get_param("BASE_URL")
    url = f"""{base_url}/cartofriches/friches/{site_id}/"""
    response = utils.get_api_response(url)
    return pd.DataFrame.from_dict(response)

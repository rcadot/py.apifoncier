import pandas as pd
from .config import get_param

from . import utils


def mutations(
    code_insee=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
    codtypbien=None,
    anneemut_min=None,
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
    result = utils.Resultat("/dvf_opendata/mutations/", **locals())
    df = result.get_dataframe()
    return df


def geomutations(
    code_insee=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
    codtypbien=None,
    anneemut_min=None,
):
    result = utils.Resultat("/dvf_opendata/geomutations/", **locals())
    gdf = result.get_geodataframe()
    return gdf


def mutation(idmutation=None):
    base_url = get_param("BASE_URL")
    url = f"""{base_url}/dvf_opendata/mutations/{idmutation}/"""
    response = utils.get_api_response(url)
    return pd.DataFrame.from_dict(response)

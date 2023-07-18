import pandas as pd
from .config import get_param

from . import utils


########################################################################
# PARCELLES
########################################################################


def parcelles(
    code_insee=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
):
    """ """
    result = utils.Resultat("/ff/parcelles/", use_token=True, **locals())
    df = result.get_dataframe()
    return df


def geoparcelles(
    code_insee=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
):
    """ """
    result = utils.Resultat("/ff/geoparcelles/", use_token=True, **locals())
    gdf = result.get_geodataframe()
    return gdf


def parcelle(idpar=None):
    """ """
    base_url = get_param("BASE_URL")
    url = f"""{base_url}/ff/parcelles/{idpar}/"""
    response = utils.get_api_response(url, use_token=True)
    return pd.DataFrame.from_dict(response)


########################################################################
# TUPS
########################################################################


def tups(
    code_insee=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
):
    """ """
    result = utils.Resultat("/ff/tups/", use_token=True, **locals())
    df = result.get_dataframe()
    return df


def geotups(
    code_insee=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
):
    """ """
    result = utils.Resultat("/ff/geotups/", use_token=True, **locals())
    gdf = result.get_geodataframe()
    return gdf


def tup(idtup=None):
    """ """
    base_url = get_param("BASE_URL")
    url = f"""{base_url}/ff/parcelles/{idtup}/"""
    response = utils.get_api_response(url, use_token=True)
    return pd.DataFrame.from_dict(response)


########################################################################
# LOCAUX
########################################################################


def locaux(
    code_insee=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
):
    """ """
    result = utils.Resultat("/ff/locaux/", use_token=True, **locals())
    df = result.get_dataframe()
    return df


def local(idlocal=None):
    """ """
    base_url = get_param("BASE_URL")
    url = f"""{base_url}/ff/locaux/{idlocal}/"""
    response = utils.get_api_response(url, use_token=True)
    return pd.DataFrame.from_dict(response)


########################################################################
# PROPRIOS
########################################################################


def proprios(
    code_insee=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
):
    """ """
    result = utils.Resultat("/ff/proprios/", use_token=True, **locals())
    df = result.get_dataframe()
    return df


def proprio(idprodroit=None):
    """ """
    base_url = get_param("BASE_URL")
    url = f"""{base_url}/ff/proprios/{idprodroit}/"""
    response = utils.get_api_response(url, use_token=True)
    return pd.DataFrame.from_dict(response)

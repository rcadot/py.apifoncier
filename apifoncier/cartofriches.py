import pandas as pd
import geopandas as gpd

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
    base_url = get_param("BASE_URL")
    geo_params = utils.process_filter_params(
        lon_lat=lon_lat,
        in_bbox=in_bbox,
        code_insee=code_insee,
        coddep=coddep,
    )
    lon_lat, in_bbox, code_insee, coddep = utils.process_geo_params(**geo_params)

    params = utils.process_filter_params(
        fields=fields,
        ordering=ordering,
        surface_min=surface_min,
        surface_max=surface_max,
        urba_zone_type=urba_zone_type,
    )

    if lon_lat:
        lon = lon_lat[0]
        lat = lon_lat[1]
        lon_min = lon - 0.01
        lon_max = lon + 0.01
        lat_min = lat - 0.01
        lat_max = lat + 0.01
        in_bbox = f"""in_bbox={lon_min},{lat_min},{lon_max},{lat_max}"""
        url = f"""{base_url}/cartofriches/friches/?{in_bbox}&contains_geom={{"type": "Point", "coordinates":[{lon}, {lat}]}}"""
        return utils.get_all_data(url, params=params)
    if in_bbox:
        url = f"""{base_url}/cartofriches/friches/?in_bbox={",".join(in_bbox)}&page_size=500"""
        return utils.get_all_data(url, params)
    if code_insee:
        datas = []
        for code in code_insee:
            url = (
                f"""{base_url}/cartofriches/friches/?code_insee={code}&page_size=500"""
            )
            data = utils.get_all_data(url, params)
            datas.append(data)
    if coddep:
        datas = []
        for code in coddep:
            url = f"""{base_url}/cartofriches/friches/?coddep={code}&page_size=500"""
            data = utils.get_all_data(url, params)
            datas.append(data)
    data = datas[0] if len(datas) == 1 else pd.concat(datas)
    return data


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
    base_url = get_param("BASE_URL")
    geo_params = utils.process_filter_params(
        lon_lat=lon_lat,
        in_bbox=in_bbox,
        code_insee=code_insee,
        coddep=coddep,
    )
    lon_lat, in_bbox, code_insee, coddep = utils.process_geo_params(**geo_params)

    params = utils.process_filter_params(
        fields=fields,
        ordering=ordering,
        surface_min=surface_min,
        surface_max=surface_max,
        urba_zone_type=urba_zone_type,
    )

    if lon_lat:
        lon = lon_lat[0]
        lat = lon_lat[1]
        lon_min = lon - 0.01
        lon_max = lon + 0.01
        lat_min = lat - 0.01
        lat_max = lat + 0.01
        in_bbox = f"""in_bbox={lon_min},{lat_min},{lon_max},{lat_max}"""
        url = f"""{base_url}/cartofriches/geofriches/?{in_bbox}&contains_geom={{"type": "Point", "coordinates":[{lon}, {lat}]}}"""
        return utils.get_all_geodata(url, params=params)
    if in_bbox:
        url = f"""{base_url}/cartofriches/geofriches/?in_bbox={",".join(in_bbox)}&page_size=500"""
        return utils.get_all_geodata(url, params)
    if code_insee:
        datas = []
        for code in code_insee:
            url = f"""{base_url}/cartofriches/geofriches/?code_insee={code}&page_size=500"""
            data = utils.get_all_geodata(url, params)
            datas.append(data)
    if coddep:
        datas = []
        for code in coddep:
            url = f"""{base_url}/cartofriches/geofriches/?coddep={code}&page_size=500"""
            data = utils.get_all_geodata(url, params)
            datas.append(data)
    data = (
        datas[0]
        if len(datas) == 1
        else gpd.GeoDataFrame(pd.concat(datas, ignore_index=True))
    )
    return data


def friche(site_id=None):
    base_url = get_param("BASE_URL")
    url = f"""{base_url}/cartofriches/friches/{site_id}/"""
    response = utils.get_api_response(url)
    return pd.DataFrame.from_dict(response)

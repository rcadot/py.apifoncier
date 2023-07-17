import warnings
import requests
import pandas as pd
import geopandas as gpd
import plotly.express as px
import geopandas as gpd
from urllib.parse import urlencode

from .config import get_param

from .exceptions import ApiDFError
from .exceptions import TokenNotConfigured

########################################################################
# INTERROGATIONS
########################################################################


def get_all_geodata(url, params=None, use_token=False):
    data_pages = []
    has_more_pages = True

    while has_more_pages:
        response = get_api_response(url, params, use_token)
        if len(response["features"]) > 0:
            data_page = gpd.GeoDataFrame.from_features(response)
            data_pages.append(data_page)

        if not response["next"]:
            has_more_pages = False
        else:
            url = response["next"]

    if data_pages:
        data = gpd.GeoDataFrame(pd.concat(data_pages, ignore_index=True))
        return data
    else:
        return None


def get_all_data(url, params=None, use_token=False):
    data_pages = []
    has_more_pages = True

    while has_more_pages:
        response = get_api_response(url, params, use_token)
        if len(response["results"]) > 0:
            data_page = pd.DataFrame(response["results"])
            data_pages.append(data_page)

        if not response["next"]:
            has_more_pages = False
        else:
            url = response["next"]

    if data_pages:
        data = pd.concat(data_pages)
        return data
    else:
        return None


def get_api_response(url, params=None, use_token=False):
    HEADERS = {
        "Content-Type": "application/json",
    }

    PROXIES = None
    proxy = get_param("PROXY")
    if proxy:
        PROXIES = {"http": proxy, "https": proxy}

    if use_token:
        token = get_param("TOKEN")
        if not token:
            raise TokenNotConfigured()
        HEADERS["Authorization"] = "Token " + token

    response = requests.get(url, params=params, headers=HEADERS, proxies=PROXIES)
    status_code = response.status_code
    if status_code != 200:
        raise ApiDFError(status_code, response.json()["detail"])

    return response.json()


########################################################################
# GESTION PARAMETRES
########################################################################


def process_filter_params(**kwargs):
    params = {}
    for kw, value in kwargs.items():
        if value is not None:
            params[kw] = value
    return params


def process_geo_params(**kwargs):
    keyword_priority = ["lon_lat", "in_bbox", "code_insee", "coddep"]
    # Vérification de l'obligation de préciser au moins un paramètre
    if not any(keyword in kwargs for keyword in keyword_priority):
        raise ValueError(
            "Veuillez préciser au moins un paramètre parmi code_insee, in_bbox, lonlat et coddep."
        )

    # Vérification si plusieurs mots-clés ont été utilisés
    used_keywords = [keyword for keyword, value in kwargs.items() if value is not None]
    for keyword in keyword_priority:
        if keyword in used_keywords:
            first_keyword = keyword
            break
    if len(used_keywords) > 1:
        warning_message = f"Les mots-clés {', '.join(used_keywords)} ont été précisés. Seul le mot-clé {first_keyword} sera utilisé."
        warnings.warn(warning_message, UserWarning)

    values = {keyword: None for keyword in keyword_priority}
    # Vérification et traitement des paramètres selon la priorité des mots-clés
    for keyword in keyword_priority:
        if keyword in kwargs:
            value = kwargs[keyword]

            if keyword == "lon_lat":
                # Vérification que in_bbox est une liste de 4 floats
                if (
                    not isinstance(value, list)
                    or len(value) != 2
                    or not all(isinstance(x, float) for x in value)
                ):
                    raise ValueError(
                        "Le paramètre lon_lat doit être une liste de 2 floats."
                    )
                values[keyword] = value
                break
            if keyword == "in_bbox":
                # Vérification que in_bbox est une liste de 4 floats
                if (
                    not isinstance(value, list)
                    or len(value) != 4
                    or not all(isinstance(x, float) for x in value)
                ):
                    raise ValueError(
                        "Le paramètre in_bbox doit être une liste de 4 floats."
                    )
                values[keyword] = value
                break
            elif keyword == "code_insee" or keyword == "coddep":
                if isinstance(value, str):
                    value = [value]
                values[keyword] = value
                break

    return tuple(values[keyword] for keyword in keyword_priority)

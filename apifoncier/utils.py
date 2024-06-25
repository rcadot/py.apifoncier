import warnings
import requests
import pandas as pd
import geopandas as gpd
from urllib.parse import urljoin

from tqdm import tqdm

from .config import get_param

from .exceptions import ApiDFError
from .exceptions import TokenNotConfigured

########################################################################
# GESTION DES RESULTATS
########################################################################


class Resultat:
    def __init__(self, url_endpoint, **kwargs):
        self.use_token = kwargs.pop("use_token", False)
        self.base_url = get_param("BASE_URL")
        self.url = urljoin(self.base_url, url_endpoint)
        self.process_params(**kwargs)

    def process_params(self, **kwargs):
        geo_params = Resultat.process_filter_params(
            lon_lat=kwargs.pop("lon_lat", None),
            in_bbox=kwargs.pop("in_bbox", None),
            code_insee=kwargs.pop("code_insee", None),
            code=kwargs.pop("code", None),
            coddep=kwargs.pop("coddep", None),
        )

        (
            self.lon_lat,
            self.in_bbox,
            self.code_insee,
            self.code,
            self.coddep,
        ) = Resultat.process_geo_params(**geo_params)
        self.params = Resultat.process_filter_params(**kwargs)
        ### On transforme les paramètres de type list en chaine de caractère concaténée
        for keyword, value in self.params.items():
            if isinstance(value, list):
                self.params[keyword] = ",".join([str(e).strip() for e in value])

    def get_dataframe(self, no_param_code=False):
        if self.lon_lat:
            lon = self.lon_lat[0]
            lat = self.lon_lat[1]
            lon_min = lon - 0.01
            lon_max = lon + 0.01
            lat_min = lat - 0.01
            lat_max = lat + 0.01
            in_bbox = f"""in_bbox={lon_min},{lat_min},{lon_max},{lat_max}"""
            url = f"""{self.url}?{in_bbox}&contains_geom={{"type": "Point", "coordinates":[{lon}, {lat}]}}"""
            return get_all_data(url, self.params, use_token=self.use_token)
        if self.in_bbox:
            url = f"""{self.url}?in_bbox={",".join(self.in_bbox)}&page_size=500"""
            return get_all_data(url, self.params, use_token=self.use_token)
        if self.code_insee:
            datas = []
            for code in self.code_insee:
                if not no_param_code:
                    url = f"""{self.url}?code_insee={code}&page_size=500"""
                else:
                    url = f"""{self.url}{code}/"""
                data = get_all_data(url, self.params, use_token=self.use_token)
                datas.append(data)
        if self.code:
            url = f"""{self.url}?code={",".join(self.code)}"""
            return get_all_data(url, self.params, use_token=self.use_token)
        if self.coddep:
            datas = []
            for code in self.coddep:
                if not no_param_code:
                    url = f"""{self.url}?coddep={code}&page_size=500"""
                else:
                    url = f"""{self.url}{code}/"""
                data = get_all_data(url, self.params, use_token=self.use_token)
                datas.append(data)
        data = datas[0] if len(datas) == 1 else pd.concat(datas, ignore_index=True)
        return data

    def get_geodataframe(self):
        if self.lon_lat:
            lon = self.lon_lat[0]
            lat = self.lon_lat[1]
            lon_min = lon - 0.01
            lon_max = lon + 0.01
            lat_min = lat - 0.01
            lat_max = lat + 0.01
            in_bbox = f"""in_bbox={lon_min},{lat_min},{lon_max},{lat_max}"""
            url = f"""{self.url}?{in_bbox}&contains_geom={{"type": "Point", "coordinates":[{lon}, {lat}]}}"""
            return get_all_geodata(url, self.params, use_token=self.use_token)
        if self.in_bbox:
            url = f"""{self.url}?in_bbox={",".join(self.in_bbox)}&page_size=500"""
            return get_all_geodata(url, self.params, use_token=self.use_token)
        if self.code_insee:
            datas = []
            for code in self.code_insee:
                url = f"""{self.url}?code_insee={code}&page_size=500"""
                data = get_all_geodata(url, self.params, use_token=self.use_token)
                datas.append(data)
        if self.coddep:
            datas = []
            for code in self.coddep:
                url = f"""{self.url}?coddep={code}&page_size=500"""
                data = get_all_geodata(url, self.params, use_token=self.use_token)
                datas.append(data)
        data = (
            datas[0]
            if len(datas) == 1
            else gpd.GeoDataFrame(pd.concat(datas, ignore_index=True))
        )
        return data

    @staticmethod
    def process_filter_params(**kwargs):
        params = {}
        for kw, value in kwargs.items():
            if value is not None:
                params[kw] = value
        return params

    @staticmethod
    def process_geo_params(**kwargs):
        keyword_priority = ["lon_lat", "in_bbox", "code_insee", "code", "coddep"]
        # Vérification de l'obligation de préciser au moins un paramètre
        if not any(keyword in kwargs for keyword in keyword_priority):
            raise ValueError(
                "Veuillez préciser au moins un paramètre parmi code_insee, code, in_bbox, lonlat et coddep."
            )

        # Vérification si plusieurs mots-clés ont été utilisés
        used_keywords = [
            keyword for keyword, value in kwargs.items() if value is not None
        ]
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
                    # Vérification que lon_lat est une liste de 2 floats
                    if (
                        not isinstance(value, list)
                        or len(value) != 2
                        or not all(is_num(x) for x in value)
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
                        or not all(is_num(x) for x in value)
                    ):
                        raise ValueError(
                            "Le paramètre in_bbox doit être une liste de 4 floats."
                        )
                    values[keyword] = [str(elt) for elt in value]
                    break
                elif keyword in ("code_insee", "code", "coddep"):
                    if isinstance(value, str):
                        value = [value]
                    values[keyword] = value
                    break

        return tuple(values[keyword] for keyword in keyword_priority)


########################################################################
# INTERROGATIONS API
########################################################################


def get_all_geodata(url, params=None, use_token=False):
    progress_bar = get_param("PROGRESS_BAR")
    data_pages = []
    has_more_pages = True

    pbar = None
    while has_more_pages:
        response = get_api_response(url, params, use_token)
        if len(response["features"]) > 0:
            data_page = gpd.GeoDataFrame.from_features(response).set_index(
                pd.json_normalize(response["features"])["id"].values
            )  ## On ajout les identifiants en index
            data_pages.append(data_page)
            if progress_bar:
                if not pbar:
                    pbar = tqdm(total=response["count"])
                    pbar.set_description(url)
                pbar.update(len(response["features"]))

        if not response["next"]:
            has_more_pages = False
        else:
            url = response["next"]

    if data_pages:
        data = gpd.GeoDataFrame(
            pd.concat(
                data_pages,
            )
        )  # ignore_index=True))
        return data
    else:
        return gpd.GeoDataFrame()


def get_all_data(url, params=None, use_token=False):
    progress_bar = get_param("PROGRESS_BAR")
    data_pages = []
    has_more_pages = True

    pbar = None
    while has_more_pages:
        response = get_api_response(url, params, use_token)
        if len(response["results"]) > 0:
            data_page = pd.DataFrame(response["results"])
            data_pages.append(data_page)
            if progress_bar:
                if not pbar:
                    pbar = tqdm(total=response["count"])
                    pbar.set_description(url)
                pbar.update(len(response["results"]))

        if not response["next"]:
            has_more_pages = False
        else:
            url = response["next"]

    if data_pages:
        data = pd.concat(data_pages)
        return data
    else:
        return pd.DataFrame()


def get_api_response(url, params=None, use_token=False, attempt=1):
    max_attempts = get_param("MAX_ATTEMPTS")
    timeout_value = get_param("TIMEOUT")
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

    try:
        response = requests.get(
            url, params=params, headers=HEADERS, proxies=PROXIES, timeout=timeout_value
        )
    except Exception as e:
        if attempt < max_attempts:
            return get_api_response(
                url, params=params, use_token=use_token, attempt=attempt + 1
            )
        else:
            raise e

    status_code = response.status_code
    if status_code != 200:
        raise ApiDFError(status_code, response.json()["detail"])

    return response.json()


def is_num(value):
    return isinstance(value, int) or isinstance(value, float)

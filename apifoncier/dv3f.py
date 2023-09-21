import pandas as pd
from .config import get_param

from . import utils


def mutations(
    code_insee=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
    anneemut_min=None,
    anneemut_max=None,
    anneemut=None,
    codtypbien=None,
    idnatmut=None,
    sbati_min=None,
    sbati_max=None,
    sterr_min=None,
    sterr_max=None,
    valeurfonc_min=None,
    valeurfonc_max=None,
    vefa=None,
    codtypprov=None,
    codtypproa=None,
    filtre=None,
):
    """Retourne les mutations issues de DV3F pour le périmètre demandée sous forme d'un dataframe

    Args:
        **code_insee (str or list, optional)**: Codes INSEE communaux ou des arrondissements municipaux. Defaults to None.

        **in_bbox (list, optional)**: Emprise rectangulaire sous la forme d'une liste [longitude_min, latitude_min, longitude_min, latitude_max] - Maximum 0.02 deg x 0.02 deg. Defaults to None.

        **lon_lat (list, optional)**: Coordonnée du point au sein de la ou des friches renvoyées [longitude, latitude]. Defaults to None.

        **fields (str, optional)**: Mettre à "all" pour obtenir tous les champs associés. Defaults to None.

        **ordering (str, optional)**: Champs à utiliser pour ordonner le résultat. Defaults to None.

        **anneemut_min (str, optional)**: Année de mutation minimale. Defaults to None.

        **anneemut_max (str, optional)**: Année de mutation maximale. Defaults to None.

        **anneemut (str, optional)**: Année de mutation. Defaults to None.

        **codtypbien (str, optional)**: Code(s) de la typologie de bien à sélectionner (il est possible de ne specifier que les premiers niveaux et de séparer par une virgule). Defaults to None.

        **idnatmut (str, optional)**: Code(s) de nature de mutation (il est possible d'en demander plusieurs en séparant par une virgule. Defaults to None.

        **sbati_min (int, optional)**: Surface batie minimale. Defaults to None.

        **sbati_max (int, optional)**: Surface batie maximale. Defaults to None.

        **sterr_min (int, optional)**: Surface de terrain minimale. Defaults to None.

        **sterr_max (int, optional)**: Surface de terrain maximale. Defaults to None.

        **valeurfonc_min (int, optional)**: Valeur foncière minimale. Defaults to None.

        **valeurfonc_max (int, optional)**: Valeur foncière maximale. Defaults to None.

        **vefa (str, optional)**: vente en l'état futur d'achevement. Defaults to None.

        **codtypprov (str, optional)** : Code(s) de la typologie du vendeur (il est possible de ne specifier que les premiers niveaux et de séparer par une virgule). Defaults to None

        **codtypproa (str, optional)** : Code(s) de la typologie de l'acheteur (il est possible de ne specifier que les premiers niveaux et de séparer par une virgule). Defaults to None

        **filtre (str, optional)**: Code alphanumerique permettant d'exclure des transactions particulières. Defaults to None.

    Returns:
        dataframe: données sur les mutations issues de DV3F
    """
    result = utils.Resultat("/dv3f/mutations/", use_token=True, **locals())
    df = result.get_dataframe()
    return df


def geomutations(
    code_insee=None,
    in_bbox=None,
    lon_lat=None,
    fields=None,
    ordering=None,
    anneemut_min=None,
    anneemut_max=None,
    anneemut=None,
    codtypbien=None,
    idnatmut=None,
    sbati_min=None,
    sbati_max=None,
    sterr_min=None,
    sterr_max=None,
    valeurfonc_min=None,
    valeurfonc_max=None,
    vefa=None,
    codtypprov=None,
    codtypproa=None,
    filtre=None,
):
    """Retourne les mutations issues de DV3F pour le périmètre demandée sous forme d'un geodataframe

    Args:
        **code_insee (str or list, optional)**: Codes INSEE communaux ou des arrondissements municipaux. Defaults to None.

        **in_bbox (list, optional)**: Emprise rectangulaire sous la forme d'une liste [longitude_min, latitude_min, longitude_min, latitude_max] - Maximum 0.02 deg x 0.02 deg. Defaults to None.

        **lon_lat (list, optional)**: Coordonnée du point au sein de la ou des friches renvoyées [longitude, latitude]. Defaults to None.

        **fields (str, optional)**: Mettre à "all" pour obtenir tous les champs associés. Defaults to None.

        **ordering (str, optional)**: Champs à utiliser pour ordonner le résultat. Defaults to None.

        **anneemut_min (str, optional)**: Année de mutation minimale. Defaults to None.

        **anneemut_max (str, optional)**: Année de mutation maximale. Defaults to None.

        **anneemut (str, optional)**: Année de mutation. Defaults to None.

        **codtypbien (str, optional)**: Code(s) de la typologie de bien à sélectionner (il est possible de ne specifier que les premiers niveaux et de séparer par une virgule). Defaults to None.

        **idnatmut (str, optional)**: Code(s) de nature de mutation (il est possible d'en demander plusieurs en séparant par une virgule. Defaults to None.

        **sbati_min (int, optional)**: Surface batie minimale. Defaults to None.

        **sbati_max (int, optional)**: Surface batie maximale. Defaults to None.

        **sterr_min (int, optional)**: Surface de terrain minimale. Defaults to None.

        **sterr_max (int, optional)**: Surface de terrain maximale. Defaults to None.

        **valeurfonc_min (int, optional)**: Valeur foncière minimale. Defaults to None.

        **valeurfonc_max (int, optional)**: Valeur foncière maximale. Defaults to None.

        **vefa (str, optional)**: vente en l'état futur d'achevement. Defaults to None.

        **codtypprov (str, optional)** : Code(s) de la typologie du vendeur (il est possible de ne specifier que les premiers niveaux et de séparer par une virgule). Defaults to None

        **codtypproa (str, optional)** : Code(s) de la typologie de l'acheteur (il est possible de ne specifier que les premiers niveaux et de séparer par une virgule). Defaults to None

        **filtre (str, optional)**: Code alphanumerique permettant d'exclure des transactions particulières. Defaults to None.

    Returns:
        geodataframe: données sur les mutations issues de DV3F avec les contours géométriques
    """
    result = utils.Resultat("/dv3f/geomutations/", use_token=True, **locals())
    gdf = result.get_geodataframe()
    return gdf


def mutation(idmutation=None):
    """Renvoie la mutation correspondant à l'identifiant idmutation (str)

    Returns:
        dataframe: donnée sur la mutation issue de DV3F
    """
    base_url = get_param("BASE_URL")
    url = f"""{base_url}/dv3f/mutations/{idmutation}/"""
    response = utils.get_api_response(url, use_token=True)
    return pd.DataFrame.from_dict([response])

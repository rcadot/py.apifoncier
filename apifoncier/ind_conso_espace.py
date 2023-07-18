import pandas as pd
from .config import get_param

from . import utils


def communes(
    code_insee=None,
    ordering=None,
    annee=None,
    annee_min=None,
    annee_max=None,
):
    """Retourne les indicateurs annuels de consommation d'espace communaux
    Args:
        **code_insee (str or list, optional)**: Codes INSEE communaux ou des arrondissements municipaux. Defaults to None.
        **ordering (str, optional)**: Champs à utiliser pour ordonner le résultat. Defaults to None.
        **annee_min (str, optional)**: Année minimale. Defaults to None.
        **annee_max(str, optional)**: Année maximale. Defaults to None.
        **annee (str, optional)**: Année. Defaults to None.

    Returns:
        dataframe: données sur la consomation d'espace
    """
    result = utils.Resultat("/indicateurs/conso_espace/communes/", **locals())
    df = result.get_dataframe(no_param_code=True)
    return df


def departements(
    coddep=None,
    ordering=None,
    annee=None,
    annee_min=None,
    annee_max=None,
):
    """Retourne les indicateurs annuels de consommation d'espace departementaux
    Args:
        **coddep (str or list, optional)**: Codes INSEE des départements. Defaults to None.
        **ordering (str, optional)**: Champs à utiliser pour ordonner le résultat. Defaults to None.
        **annee_min (str, optional)**: Année minimale. Defaults to None.
        **annee_max(str, optional)**: Année maximale. Defaults to None.
        **annee (str, optional)**: Année. Defaults to None.

    Returns:
        dataframe: données sur la consommation d'espace
    """
    result = utils.Resultat("/indicateurs/conso_espace/departements/", **locals())
    df = result.get_dataframe(no_param_code=True)
    return df

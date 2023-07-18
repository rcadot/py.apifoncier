import pandas as pd
from .config import get_param

from . import utils


def aav(
    code_insee=None,
    ordering=None,
    annee=None,
    periode="annuel",
):
    """Retourne les indicateurs annuels ou triennaux de prix à l'aire d'attraction de la ville
    Args:
        **code_insee (str or list, optional)**: Codes INSEE des AAV. Defaults to None.
        **ordering (str, optional)**: Champs à utiliser pour ordonner le résultat. Defaults to None.
        **annee (str, optional)**: Année. Defaults to None.
        **periode (str, optional)**: Prend la valeur "annuel" ou "triennal". Defaults to annuel.

    Returns:
        dataframe: données sur les marchés immobiliers
    """
    if not periode in ("annuel", "triennal"):
        raise ValueError("Le paramètre periode doit valoir 'annuel' ou 'triennal'.")
    result = utils.Resultat(f"/indicateurs/dv3f/aav/{periode}/", **locals())
    df = result.get_dataframe(no_param_code=True)
    return df


def communes(
    code_insee=None,
    ordering=None,
    annee=None,
    periode="annuel",
):
    """Retourne les indicateurs annuels ou triennaux de prix à la commune
    Args:
        **code_insee (str or list, optional)**: Codes INSEE communaux ou des arrondissements municipaux. Defaults to None.
        **ordering (str, optional)**: Champs à utiliser pour ordonner le résultat. Defaults to None.
        **annee (str, optional)**: Année. Defaults to None.
        **periode (str, optional)**: Prend la valeur "annuel" ou "triennal". Defaults to annuel.

    Returns:
        dataframe: données sur les marchés immobiliers
    """
    if not periode in ("annuel", "triennal"):
        raise ValueError("Le paramètre periode doit valoir 'annuel' ou 'triennal'.")
    result = utils.Resultat(f"/indicateurs/dv3f/communes/{periode}/", **locals())
    df = result.get_dataframe(no_param_code=True)
    return df


def departements(
    coddep=None,
    ordering=None,
    annee=None,
    periode="annuel",
):
    """Retourne les indicateurs annuels ou triennaux de prix à l'EPCI
    Args:
        **coddep (str or list, optional)**: Codes des départements. Defaults to None.
        **ordering (str, optional)**: Champs à utiliser pour ordonner le résultat. Defaults to None.
        **annee (str, optional)**: Année. Defaults to None.
        **periode (str, optional)**: Prend la valeur "annuel" ou "triennal". Defaults to annuel.

    Returns:
        dataframe: données sur les marchés immobiliers
    """
    if not periode in ("annuel", "triennal"):
        raise ValueError("Le paramètre periode doit valoir 'annuel' ou 'triennal'.")
    result = utils.Resultat(f"/indicateurs/dv3f/departements/{periode}/", **locals())
    df = result.get_dataframe(no_param_code=True)
    return df


def epci(
    code_insee=None,
    ordering=None,
    annee=None,
    periode="annuel",
):
    """Retourne les indicateurs annuels ou triennaux de prix à l'EPCI
    Args:
        **code_insee (str or list, optional)**: Codes INSEE des EPCI. Defaults to None.
        **ordering (str, optional)**: Champs à utiliser pour ordonner le résultat. Defaults to None.
        **annee (str, optional)**: Année. Defaults to None.
        **periode (str, optional)**: Prend la valeur "annuel" ou "triennal". Defaults to annuel.

    Returns:
        dataframe: données sur les marchés immobiliers
    """
    if not periode in ("annuel", "triennal"):
        raise ValueError("Le paramètre periode doit valoir 'annuel' ou 'triennal'.")
    result = utils.Resultat(f"/indicateurs/dv3f/epci/{periode}/", **locals())
    df = result.get_dataframe(no_param_code=True)
    return df


def regions(
    code_insee=None,
    ordering=None,
    annee=None,
    periode="annuel",
):
    """Retourne les indicateurs annuels ou triennaux de prix à la région
    Args:
        **code_insee (str or list, optional)**: Codes INSEE des régions. Defaults to None.
        **ordering (str, optional)**: Champs à utiliser pour ordonner le résultat. Defaults to None.
        **annee (str, optional)**: Année. Defaults to None.
        **periode (str, optional)**: Prend la valeur "annuel" ou "triennal". Defaults to annuel.

    Returns:
        dataframe: données sur les marchés immobiliers
    """
    if not periode in ("annuel", "triennal"):
        raise ValueError("Le paramètre periode doit valoir 'annuel' ou 'triennal'.")
    result = utils.Resultat(f"/indicateurs/dv3f/regions/{periode}/", **locals())
    df = result.get_dataframe(no_param_code=True)
    return df

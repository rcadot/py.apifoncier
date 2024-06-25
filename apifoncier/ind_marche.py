import pandas as pd
from .config import get_param

from . import utils


def prix_volume(
    echelle=None,
    code=None,
    ordering=None,
    annee=None,
    periode="annuel",
):
    """Retourne les indicateurs annuels ou triennaux de prix et de volume pour les entités de l'échelle geographique définie

    Args:
        **echelle (str, required)**: Echelle géographique souhaitée parmi communes / epci / aav / departements / regions / france

        **code (str or list, required)**: Codes INSEE des entités géographiques. Defaults to None.

        **ordering (str, optional)**: Champs à utiliser pour ordonner le résultat. Defaults to None.

        **annee (str, optional)**: Année. Defaults to None.

        **periode (str, optional)**: Prend la valeur "annuel" ou "triennal". Defaults to annuel.

    Returns:
        dataframe: données de prix et de volume sur les marchés immobiliers

    Examples:
        >>> import apifoncier.ind_marche as marche
        >>> marche.prix_volume(echelle="communes", code="59350")
        >>> marche.prix_volume(echelle="departements", code=["62", "59"], annee="2020")
        >>> marche.prix_volume(echelle="aav", code=["001", "002"], periode="triennal")
    """
    if not periode in ("annuel", "triennal"):
        raise ValueError("Le paramètre periode doit valoir 'annuel' ou 'triennal'.")
    result = utils.Resultat(f"/indicateurs/dv3f/prix/{periode}/", **locals())
    df = result.get_dataframe()
    return df


def activite(
    echelle=None,
    code=None,
    ordering=None,
    annee=None,
):
    """Retourne les indicateurs d'activité de marché pour les entités de l'échelle geographique définie

    Args:
        **echelle (str, required)**: Echelle géographique souhaitée parmi communes / epci / aav / departements / regions / france

        **code (str or list, required)**: Codes INSEE des entités géographiques. Defaults to None.

        **ordering (str, optional)**: Champs à utiliser pour ordonner le résultat. Defaults to None.

        **annee (str, optional)**: Année. Defaults to None.

    Returns:
        dataframe: données d'activité sur les marchés immobiliers

    Examples:
        >>> import apifoncier.ind_marche as marche
        >>> marche.activite_marche(echelle="communes", code="59350")
        >>> marche.activite_marche(echelle="departements", code=["62", "59"], annee="2020")
        >>> marche.activite_marche(echelle="aav", code=["001", "002"])
    """
    result = utils.Resultat(f"/indicateurs/dv3f/activite/", **locals())
    df = result.get_dataframe()
    return df


def accessibilite(
    code=None,
    ordering=None,
    annee=None,
):
    """Retourne les indicateurs d'accessibilité de marché pour toutes les communes des AAV définis

    Args:
        **code (str or list, required)**: Codes INSEE de l'AAV. Defaults to None.

        **ordering (str, optional)**: Champs à utiliser pour ordonner le résultat. Defaults to None.

        **annee (str, optional)**: Année. Defaults to None.

    Returns:
        dataframe: données d'accessibilité des communes sur les marchés immobiliers

    Examples:
        >>> import apifoncier.ind_marche as marche
        >>> marche.accessibilite(code="001")
        >>> marche.accessibilite(echelle="aav", code=["001", "002"])
    """
    result = utils.Resultat(f"/indicateurs/dv3f/accessibilite/", **locals())
    df = result.get_dataframe()
    return df


def valorisation(
    echelle=None,
    code_insee=None,
    ordering=None,
    annee=None,
):
    """Retourne les indicateurs de valorisation communale à l'aire d'attraction de la ville ou à l'EPCI

    Args:
        **echelle (str, required)**: Echelle géographique souhaitée parmi epci / aav

        **code_insee (str or list, required)**: Codes INSEE des AAV ou de l'EPCI. Defaults to None.

        **ordering (str, optional)**: Champs à utiliser pour ordonner le résultat. Defaults to None.

        **annee (str, optional)**: Année. Defaults to None.

    Returns:
        dataframe: données sur les valorisations communales

    Examples:
        >>> import apifoncier.ind_marche as marche
        >>> marche.valorisation(echelle="aav", code_insee="001")
        >>> marche.valorisation(echelle="aav", code_insee=["001", "002"], annee=2020)
    """
    if not echelle in ("aav", "epci"):
        raise ValueError("Le paramètre echelle doit valoir 'aav' ou 'epci'.")
    result = utils.Resultat(f"/indicateurs/dv3f/valorisation/{echelle}/", **locals())
    df = result.get_dataframe(no_param_code=True)
    return df

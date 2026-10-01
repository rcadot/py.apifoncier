"""Indicateurs de marché immobilier issus de DV3F (accès libre).

Endpoints interrogés :

* ``/indicateurs/dv3f/prix/<periode>/`` : prix et volumes ;
* ``/indicateurs/dv3f/activite/`` : activité de marché ;
* ``/indicateurs/dv3f/accessibilite/`` : accessibilité financière ;
* ``/indicateurs/dv3f/valorisation/<echelle>/<code>/`` : valorisation communale.
"""

from __future__ import annotations

from typing import Optional, Union

from ._query import Codes, Table, fetch
from .exceptions import ValidationError

ECHELLES = ("communes", "epci", "aav", "departements", "regions", "france")
ECHELLES_VALORISATION = ("aav", "epci")
PERIODES = ("annuel", "triennal")


def _check_choice(name: str, value: Optional[str], choices: tuple) -> str:
    """Contrôle qu'une valeur appartient à une liste de choix.

    Args:
        name: Nom du paramètre, pour le message d'erreur.
        value: Valeur fournie.
        choices: Valeurs admises.

    Returns:
        La valeur contrôlée.

    Raises:
        ValidationError: Si la valeur n'est pas admise.
    """
    if value is None or value not in choices:
        raise ValidationError(
            f"Le paramètre {name} doit valoir {' / '.join(repr(c) for c in choices)}."
        )
    return value


def prix_volume(
    echelle: Optional[str] = None,
    code: Codes = None,
    ordering: Optional[str] = None,
    annee: Optional[Union[int, str]] = None,
    periode: str = "annuel",
) -> Table:
    """Retourne les indicateurs annuels ou triennaux de prix et de volume.

    Args:
        echelle: Échelle géographique parmi ``communes``, ``epci``, ``aav``,
            ``departements``, ``regions`` et ``france`` (requis).
        code: Code(s) des entités géographiques (requis), regroupés par lots
            de 10 par requête.
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        annee: Année (année centrale pour la période triennale).
        periode: ``"annuel"`` (par défaut) ou ``"triennal"``.

    Returns:
        Un tableau des indicateurs de prix et de volume.

    Examples:
        >>> import apifoncier.ind_marche as marche
        >>> marche.prix_volume(echelle="communes", code="59350")
        >>> marche.prix_volume(echelle="departements", code=["62", "59"], annee=2020)
        >>> marche.prix_volume(echelle="aav", code=["001", "002"], periode="triennal")
    """
    _check_choice("echelle", echelle, ECHELLES)
    _check_choice("periode", periode, PERIODES)
    params = {"echelle": echelle, "code": code, "ordering": ordering, "annee": annee}
    return fetch(f"/indicateurs/dv3f/prix/{periode}/", params)


def activite(
    echelle: Optional[str] = None,
    code: Codes = None,
    ordering: Optional[str] = None,
    annee: Optional[Union[int, str]] = None,
) -> Table:
    """Retourne les indicateurs triennaux d'activité du marché.

    Args:
        echelle: Échelle géographique parmi ``communes``, ``epci``, ``aav``,
            ``departements``, ``regions`` et ``france`` (requis).
        code: Code(s) des entités géographiques (requis).
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        annee: Année centrale de la période de trois ans.

    Returns:
        Un tableau des indicateurs d'activité.

    Examples:
        >>> import apifoncier.ind_marche as marche
        >>> marche.activite(echelle="communes", code="59350")
        >>> marche.activite(echelle="departements", code=["62", "59"], annee=2020)
    """
    _check_choice("echelle", echelle, ECHELLES)
    params = {"echelle": echelle, "code": code, "ordering": ordering, "annee": annee}
    return fetch("/indicateurs/dv3f/activite/", params)


def accessibilite(
    code: Codes = None,
    ordering: Optional[str] = None,
    annee: Optional[Union[int, str]] = None,
) -> Table:
    """Retourne les indicateurs d'accessibilité financière des communes des AAV demandées.

    Args:
        code: Code(s) INSEE des aires d'attraction des villes (requis).
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        annee: Année.

    Returns:
        Un tableau des indicateurs d'accessibilité.

    Examples:
        >>> import apifoncier.ind_marche as marche
        >>> marche.accessibilite(code="001")
        >>> marche.accessibilite(code=["001", "002"])
    """
    params = dict(locals())
    return fetch("/indicateurs/dv3f/accessibilite/", params)


def valorisation(
    echelle: Optional[str] = None,
    code_insee: Codes = None,
    ordering: Optional[str] = None,
    annee: Optional[Union[int, str]] = None,
) -> Table:
    """Retourne les indicateurs de valorisation des communes dans leur AAV ou leur EPCI.

    Args:
        echelle: ``"aav"`` ou ``"epci"`` (requis).
        code_insee: Code(s) des AAV ou des EPCI (requis).
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        annee: Année centrale de la période de trois ans.

    Returns:
        Un tableau des indicateurs de valorisation.

    Examples:
        >>> import apifoncier.ind_marche as marche
        >>> marche.valorisation(echelle="aav", code_insee="001")
        >>> marche.valorisation(echelle="aav", code_insee=["001", "002"], annee=2020)
    """
    _check_choice("echelle", echelle, ECHELLES_VALORISATION)
    params = {"code_insee": code_insee, "ordering": ordering, "annee": annee}
    return fetch(f"/indicateurs/dv3f/valorisation/{echelle}/", params, path_code=True)

"""Indicateurs de prix issus de DV3F, par échelle géographique (accès libre).

Endpoints interrogés : ``/indicateurs/dv3f/<echelle>/<periode>/<code>/``, où
``echelle`` vaut ``aav``, ``communes``, ``departements``, ``epci`` ou ``regions``
et ``periode`` vaut ``annuel`` ou ``triennal``.

Le module :mod:`apifoncier.ind_marche` propose des indicateurs plus complets
(prix et volumes, activité, accessibilité, valorisation).
"""

from __future__ import annotations

from typing import Optional, Union

from ._query import Codes, Table, fetch
from .exceptions import ValidationError

PERIODES = ("annuel", "triennal")


def _check_periode(periode: str) -> str:
    """Contrôle la période demandée.

    Args:
        periode: ``"annuel"`` ou ``"triennal"``.

    Returns:
        La période contrôlée.

    Raises:
        ValidationError: Si la période n'est pas reconnue.
    """
    if periode not in PERIODES:
        raise ValidationError(
            "Le paramètre periode doit valoir 'annuel' ou 'triennal'."
        )
    return periode


def _fetch_prix(
    echelle: str,
    code_param: str,
    codes: Codes,
    ordering: Optional[str],
    annee: Optional[Union[int, str]],
    periode: str,
    paginate: bool = True,
    output: Optional[str] = None,
) -> Table:
    """Interroge l'endpoint de prix d'une échelle géographique.

    Args:
        echelle: Segment d'URL de l'échelle (``communes``, ``aav``...).
        code_param: Nom du paramètre de code exposé à l'utilisateur.
        codes: Code(s) géographique(s).
        ordering: Champ(s) de tri.
        annee: Année.
        periode: ``"annuel"`` ou ``"triennal"``.
        paginate: ``False`` pour ne récupérer que la première page.
        output: ``"pandas"``, ``"polars"`` ou ``"dict"`` ; par défaut ``OUTPUT_FORMAT``.

    Returns:
        Un tableau des indicateurs de prix.
    """
    endpoint = f"/indicateurs/dv3f/{echelle}/{_check_periode(periode)}/"
    params = {
        code_param: codes,
        "ordering": ordering,
        "annee": annee,
        "paginate": paginate,
        "output": output,
    }
    return fetch(endpoint, params, path_code=True)


def aav(
    code_insee: Codes = None,
    ordering: Optional[str] = None,
    annee: Optional[Union[int, str]] = None,
    periode: str = "annuel",
    paginate: bool = True,
    output: Optional[str] = None,
) -> Table:
    """Retourne les indicateurs annuels ou triennaux de prix des aires d'attraction des villes.

    Args:
        code_insee: Code(s) INSEE des AAV (requis).
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        annee: Année.
        periode: ``"annuel"`` (par défaut) ou ``"triennal"``.
        paginate: ``False`` pour ne récupérer que la première page.
        output: ``"pandas"``, ``"polars"`` ou ``"dict"`` ; par défaut ``OUTPUT_FORMAT``.

    Returns:
        Un tableau des indicateurs de prix.

    Examples:
        >>> import apifoncier.ind_prix as prix
        >>> prix.aav(code_insee="001")
        >>> prix.aav(code_insee=["001", "002"], periode="triennal")
    """
    return _fetch_prix(
        "aav", "code_insee", code_insee, ordering, annee, periode, paginate, output
    )


def communes(
    code_insee: Codes = None,
    ordering: Optional[str] = None,
    annee: Optional[Union[int, str]] = None,
    periode: str = "annuel",
    paginate: bool = True,
    output: Optional[str] = None,
) -> Table:
    """Retourne les indicateurs annuels ou triennaux de prix des communes.

    Args:
        code_insee: Code(s) INSEE communaux ou d'arrondissements municipaux (requis).
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        annee: Année.
        periode: ``"annuel"`` (par défaut) ou ``"triennal"``.
        paginate: ``False`` pour ne récupérer que la première page.
        output: ``"pandas"``, ``"polars"`` ou ``"dict"`` ; par défaut ``OUTPUT_FORMAT``.

    Returns:
        Un tableau des indicateurs de prix.

    Examples:
        >>> import apifoncier.ind_prix as prix
        >>> prix.communes(code_insee="59350")
        >>> prix.communes(code_insee=["59350", "59646"], annee=2020)
    """
    return _fetch_prix(
        "communes", "code_insee", code_insee, ordering, annee, periode, paginate, output
    )


def departements(
    coddep: Codes = None,
    ordering: Optional[str] = None,
    annee: Optional[Union[int, str]] = None,
    periode: str = "annuel",
    paginate: bool = True,
    output: Optional[str] = None,
) -> Table:
    """Retourne les indicateurs annuels ou triennaux de prix des départements.

    Args:
        coddep: Code(s) des départements (requis).
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        annee: Année.
        periode: ``"annuel"`` (par défaut) ou ``"triennal"``.
        paginate: ``False`` pour ne récupérer que la première page.
        output: ``"pandas"``, ``"polars"`` ou ``"dict"`` ; par défaut ``OUTPUT_FORMAT``.

    Returns:
        Un tableau des indicateurs de prix.

    Examples:
        >>> import apifoncier.ind_prix as prix
        >>> prix.departements(coddep=["59", "62"], periode="triennal")
    """
    return _fetch_prix(
        "departements", "coddep", coddep, ordering, annee, periode, paginate, output
    )


def epci(
    code_insee: Codes = None,
    ordering: Optional[str] = None,
    annee: Optional[Union[int, str]] = None,
    periode: str = "annuel",
    paginate: bool = True,
    output: Optional[str] = None,
) -> Table:
    """Retourne les indicateurs annuels ou triennaux de prix des EPCI.

    Args:
        code_insee: Code(s) SIREN des EPCI (requis).
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        annee: Année.
        periode: ``"annuel"`` (par défaut) ou ``"triennal"``.
        paginate: ``False`` pour ne récupérer que la première page.
        output: ``"pandas"``, ``"polars"`` ou ``"dict"`` ; par défaut ``OUTPUT_FORMAT``.

    Returns:
        Un tableau des indicateurs de prix.

    Examples:
        >>> import apifoncier.ind_prix as prix
        >>> prix.epci(code_insee="200093201")
    """
    return _fetch_prix(
        "epci", "code_insee", code_insee, ordering, annee, periode, paginate, output
    )


def regions(
    code_insee: Codes = None,
    ordering: Optional[str] = None,
    annee: Optional[Union[int, str]] = None,
    periode: str = "annuel",
    paginate: bool = True,
    output: Optional[str] = None,
) -> Table:
    """Retourne les indicateurs annuels ou triennaux de prix des régions.

    Args:
        code_insee: Code(s) INSEE des régions (requis).
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        annee: Année.
        periode: ``"annuel"`` (par défaut) ou ``"triennal"``.
        paginate: ``False`` pour ne récupérer que la première page.
        output: ``"pandas"``, ``"polars"`` ou ``"dict"`` ; par défaut ``OUTPUT_FORMAT``.

    Returns:
        Un tableau des indicateurs de prix.

    Examples:
        >>> import apifoncier.ind_prix as prix
        >>> prix.regions(code_insee=["32", "11"], annee=2020)
    """
    return _fetch_prix(
        "regions", "code_insee", code_insee, ordering, annee, periode, paginate, output
    )

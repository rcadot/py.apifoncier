"""Indicateurs annuels de consommation d'espaces naturels, agricoles et forestiers (accès libre).

Endpoints interrogés :

* ``/indicateurs/conso_espace/communes/<code_insee>/`` ;
* ``/indicateurs/conso_espace/departements/<coddep>/``.
"""

from __future__ import annotations

from typing import Optional, Union

from ._query import Codes, Table, fetch


def communes(
    code_insee: Codes = None,
    ordering: Optional[str] = None,
    annee: Optional[Union[int, str]] = None,
    annee_min: Optional[Union[int, str]] = None,
    annee_max: Optional[Union[int, str]] = None,
    paginate: bool = True,
    output: Optional[str] = None,
) -> Table:
    """Retourne les indicateurs annuels de consommation d'espace des communes.

    Args:
        code_insee: Code(s) INSEE communaux ou d'arrondissements municipaux (requis).
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        annee: Année.
        annee_min: Année minimale (incluse).
        annee_max: Année maximale (incluse).
        paginate: ``False`` pour ne récupérer que la première page.
        output: ``"pandas"``, ``"polars"`` ou ``"dict"`` ; par défaut ``OUTPUT_FORMAT``.

    Returns:
        Un tableau des indicateurs (``pandas`` ou ``polars`` selon ``OUTPUT_FORMAT``).

    Examples:
        >>> import apifoncier.ind_conso_espace as conso_enaf
        >>> conso_enaf.communes(code_insee="59350")
        >>> conso_enaf.communes(code_insee=["59350", "62041"], annee_min=2015)
    """
    params = dict(locals())
    return fetch("/indicateurs/conso_espace/communes/", params, path_code=True)


def departements(
    coddep: Codes = None,
    ordering: Optional[str] = None,
    annee: Optional[Union[int, str]] = None,
    annee_min: Optional[Union[int, str]] = None,
    annee_max: Optional[Union[int, str]] = None,
    paginate: bool = True,
    output: Optional[str] = None,
) -> Table:
    """Retourne les indicateurs annuels de consommation d'espace des départements.

    Args:
        coddep: Code(s) INSEE départementaux (requis).
        ordering: Champ(s) de tri, préfixé(s) de ``-`` pour un tri décroissant.
        annee: Année.
        annee_min: Année minimale (incluse).
        annee_max: Année maximale (incluse).
        paginate: ``False`` pour ne récupérer que la première page.
        output: ``"pandas"``, ``"polars"`` ou ``"dict"`` ; par défaut ``OUTPUT_FORMAT``.

    Returns:
        Un tableau des indicateurs (``pandas`` ou ``polars`` selon ``OUTPUT_FORMAT``).

    Examples:
        >>> import apifoncier.ind_conso_espace as conso_enaf
        >>> conso_enaf.departements(coddep="59")
        >>> conso_enaf.departements(coddep=["59", "62"], annee_max=2015)
    """
    params = dict(locals())
    return fetch("/indicateurs/conso_espace/departements/", params, path_code=True)

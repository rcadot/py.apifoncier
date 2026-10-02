"""Fonctions utilitaires conservées pour compatibilité ascendante.

Le traitement des requêtes est désormais assuré par les modules internes
``apifoncier._http`` (transport) et ``apifoncier._query`` (construction des
requêtes et assemblage des résultats). Ce module ré-expose les points
d'entrée historiques, utilisés notamment par des scripts existants.
"""

from __future__ import annotations

from typing import Any, Dict, Mapping, Optional, Union

import geopandas as gpd
import pandas as pd

from ._http import get_api_response
from ._query import (
    BBOX_MAX_DEFAULT,
    collect,
    fetch,
    is_num,
    to_geodataframe,
    to_table,
)

__all__ = [
    "Resultat",
    "get_all_data",
    "get_all_geodata",
    "get_api_response",
    "is_num",
]


def get_all_data(
    url: str, params: Optional[Mapping[str, Any]] = None, use_token: bool = False
) -> Any:
    """Récupère toutes les pages d'une ressource tabulaire.

    Args:
        url: URL complète de la première page.
        params: Paramètres de la requête.
        use_token: ``True`` pour les endpoints à accès restreint.

    Returns:
        Un tableau au format défini par ``OUTPUT_FORMAT``.
    """
    return to_table(_collect_url(url, params, use_token))


def get_all_geodata(
    url: str, params: Optional[Mapping[str, Any]] = None, use_token: bool = False
) -> gpd.GeoDataFrame:
    """Récupère toutes les pages d'une ressource GeoJSON.

    Args:
        url: URL complète de la première page.
        params: Paramètres de la requête.
        use_token: ``True`` pour les endpoints à accès restreint.

    Returns:
        Un ``GeoDataFrame`` indexé par les identifiants des entités.
    """
    return to_geodataframe(_collect_url(url, params, use_token))


def _collect_url(
    url: str, params: Optional[Mapping[str, Any]], use_token: bool
) -> list:
    """Parcourt toutes les pages d'une URL absolue.

    Args:
        url: URL complète de la première page.
        params: Paramètres de la requête.
        use_token: ``True`` pour les endpoints à accès restreint.

    Returns:
        La liste des enregistrements de toutes les pages.
    """
    return collect([(url, dict(params or {}))], use_token=use_token)


class Resultat:
    """Requête paramétrée sur un endpoint de liste (interface historique).

    Préférer l'usage direct des fonctions des modules thématiques
    (:mod:`apifoncier.ff`, :mod:`apifoncier.dvf_opendata`, etc.) ou de
    :func:`apifoncier.get`.

    Attributes:
        endpoint: Chemin de l'endpoint.
        use_token: ``True`` pour les endpoints à accès restreint.
        params: Paramètres de l'appel.
    """

    def __init__(self, url_endpoint: str, **kwargs: Any) -> None:
        """Initialise la requête.

        Args:
            url_endpoint: Chemin de l'endpoint, terminé par ``/``.
            **kwargs: Paramètres de l'appel ; ``use_token`` est extrait.
        """
        self.use_token: bool = bool(kwargs.pop("use_token", False))
        self.endpoint = url_endpoint
        self.params: Dict[str, Any] = kwargs

    def get_dataframe(self, no_param_code: bool = False) -> Union[pd.DataFrame, Any]:
        """Exécute la requête et renvoie un tableau.

        Args:
            no_param_code: ``True`` si le code fait partie du chemin.

        Returns:
            Un tableau au format défini par ``OUTPUT_FORMAT``.
        """
        return fetch(
            self.endpoint,
            self.params,
            use_token=self.use_token,
            path_code=no_param_code,
            max_bbox=BBOX_MAX_DEFAULT,
        )

    def get_geodataframe(self) -> gpd.GeoDataFrame:
        """Exécute la requête et renvoie un ``GeoDataFrame``.

        Returns:
            Le ``GeoDataFrame`` des entités renvoyées.
        """
        return fetch(
            self.endpoint,
            self.params,
            use_token=self.use_token,
            geo=True,
            max_bbox=BBOX_MAX_DEFAULT,
        )

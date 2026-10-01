"""Client Python de l'API Données foncières du Cerema.

Modules thématiques :

* :mod:`apifoncier.cartofriches` : friches (accès libre) ;
* :mod:`apifoncier.dvf_opendata` : mutations DVF+ (accès libre) ;
* :mod:`apifoncier.dv3f` : mutations DV3F (accès restreint) ;
* :mod:`apifoncier.ff` : Fichiers fonciers (accès restreint) ;
* :mod:`apifoncier.ind_conso_espace` : consommation d'espace (accès libre) ;
* :mod:`apifoncier.ind_prix` et :mod:`apifoncier.ind_marche` : indicateurs
  de marché immobilier (accès libre).

Examples:
    >>> import apifoncier
    >>> apifoncier.configure(TOKEN="mon_jeton")
    >>> import apifoncier.ff as ff
    >>> ff.parcelles(code_insee="59350")
"""

from __future__ import annotations

import re
from typing import Any, Optional

__version__ = "0.1.0"

from . import config
from ._http import close_session
from ._query import BBOX_MAX_DEFAULT, fetch
from .config import configure, get_config, reset
from .exceptions import (
    ApiDFError,
    ApiFoncierError,
    AuthenticationError,
    InsecureTransportError,
    TokenNotConfigured,
    ValidationError,
)

# Chemin d'endpoint : segments alphanumériques séparés par « / ».
_ENDPOINT_PATTERN = re.compile(r"(/[A-Za-z0-9_-]+)+/?")


def get(
    endpoint: str,
    *,
    geo: bool = False,
    use_token: bool = False,
    path_code: bool = False,
    max_bbox: Optional[float] = BBOX_MAX_DEFAULT,
    **params: Any,
) -> Any:
    """Interroge librement un endpoint de liste de l'API.

    Cette fonction générique donne accès aux endpoints qui ne disposent pas
    encore d'une fonction dédiée, avec les mêmes garanties (pagination,
    nouvelles tentatives, contrôle des paramètres de localisation).

    Args:
        endpoint: Chemin de l'endpoint, par exemple ``"/ff/parcelles/"``.
        geo: ``True`` pour un endpoint GeoJSON (renvoie un ``GeoDataFrame``).
        use_token: ``True`` pour un endpoint à accès restreint.
        path_code: ``True`` si le code géographique fait partie du chemin.
        max_bbox: Taille maximale de l'emprise ``in_bbox`` en degrés
            (``None`` pour ne pas contrôler).
        **params: Paramètres de la requête ; ``lon_lat``, ``in_bbox``,
            ``code_insee``, ``code`` ou ``coddep`` sont traités comme
            paramètres de localisation.

    Returns:
        Un ``GeoDataFrame`` si ``geo`` est vrai, sinon un tableau au format
        défini par ``OUTPUT_FORMAT``.

    Raises:
        ValidationError: Si l'endpoint ou un paramètre est invalide.

    Examples:
        >>> import apifoncier
        >>> apifoncier.get("/cartofriches/friches/", code_insee="59350")
        >>> apifoncier.get("/ff/geotups/", geo=True, use_token=True, code_insee="59350")
    """
    if not _ENDPOINT_PATTERN.fullmatch(endpoint):
        raise ValidationError(
            f"endpoint invalide : {endpoint!r} (chemin attendu, ex. '/ff/parcelles/')."
        )
    if not endpoint.endswith("/"):
        endpoint += "/"
    location_required = any(
        key in params for key in ("lon_lat", "in_bbox", "code_insee", "code", "coddep")
    )
    return fetch(
        endpoint,
        params,
        use_token=use_token,
        geo=geo,
        path_code=path_code,
        max_bbox=max_bbox,
        location_required=location_required,
    )


from . import (
    cartofriches,
    dv3f,
    dvf_opendata,
    ff,
    ind_conso_espace,
    ind_marche,
    ind_prix,
)

__all__ = [
    "ApiDFError",
    "ApiFoncierError",
    "AuthenticationError",
    "InsecureTransportError",
    "TokenNotConfigured",
    "ValidationError",
    "__version__",
    "cartofriches",
    "close_session",
    "config",
    "configure",
    "dv3f",
    "dvf_opendata",
    "ff",
    "get",
    "get_config",
    "ind_conso_espace",
    "ind_marche",
    "ind_prix",
    "reset",
]

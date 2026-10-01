"""Couche de transport HTTP vers l'API Données foncières.

Ce module centralise :

* la session :class:`requests.Session` partagée (réutilisation des connexions) ;
* la stratégie de nouvelles tentatives avec attente exponentielle, appliquée
  aux erreurs réseau et aux codes 429, 500, 502, 503 et 504 ;
* l'authentification par jeton, envoyée uniquement en HTTPS et uniquement
  vers l'hôte configuré dans ``BASE_URL`` ;
* la conversion des réponses d'erreur en exceptions explicites ;
* le parcours des pages de résultats.
"""

from __future__ import annotations

import logging
import threading
from typing import Any, Dict, Iterator, List, Mapping, Optional, Tuple
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from . import config
from .exceptions import (
    ApiDFError,
    ApiFoncierError,
    AuthenticationError,
    InsecureTransportError,
    TokenNotConfigured,
)

logger = logging.getLogger("apifoncier")

RETRY_STATUS = (429, 500, 502, 503, 504)
_MAX_DETAIL_LENGTH = 300

_lock = threading.Lock()
_session: Optional[requests.Session] = None
_session_generation = -1


def _user_agent() -> str:
    """Construit l'en-tête ``User-Agent`` envoyé à l'API.

    Returns:
        Une chaîne de la forme ``apifoncier-python/<version>``.
    """
    from . import __version__

    return f"apifoncier-python/{__version__}"


def _build_session() -> requests.Session:
    """Crée une session HTTP configurée selon les paramètres courants.

    Returns:
        Une session avec en-têtes, proxy et stratégie de nouvelles tentatives.
    """
    session = requests.Session()
    session.headers.update({"Accept": "application/json", "User-Agent": _user_agent()})
    retry = Retry(
        total=config.get_param("MAX_ATTEMPTS") - 1,
        backoff_factor=config.get_param("BACKOFF_FACTOR"),
        status_forcelist=RETRY_STATUS,
        allowed_methods=frozenset({"GET"}),
        respect_retry_after_header=True,
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    proxy = config.get_param("PROXY")
    if proxy:
        session.proxies.update({"http": proxy, "https": proxy})
    return session


def get_session() -> requests.Session:
    """Renvoie la session partagée, reconstruite si la configuration a changé.

    Returns:
        La session HTTP à utiliser pour les requêtes.
    """
    global _session, _session_generation
    with _lock:
        if _session is None or _session_generation != config.generation():
            if _session is not None:
                _session.close()
            _session = _build_session()
            _session_generation = config.generation()
        return _session


def close_session() -> None:
    """Ferme la session partagée et libère les connexions ouvertes."""
    global _session
    with _lock:
        if _session is not None:
            _session.close()
            _session = None


def _same_origin(url: str, reference: str) -> bool:
    """Indique si deux URL partagent le même hôte (et le même port).

    Args:
        url: URL à tester.
        reference: URL de référence.

    Returns:
        ``True`` si les deux URL désignent le même hôte.
    """
    return urlparse(url).netloc.lower() == urlparse(reference).netloc.lower()


def _auth_headers(url: str) -> Dict[str, str]:
    """Construit l'en-tête d'authentification après contrôles de sécurité.

    Args:
        url: URL complète de la requête.

    Returns:
        Un dictionnaire contenant l'en-tête ``Authorization``.

    Raises:
        TokenNotConfigured: Si aucun jeton n'est disponible.
        InsecureTransportError: Si l'URL n'est pas en HTTPS ou ne désigne pas
            l'hôte configuré dans ``BASE_URL``.
    """
    token = config.get_token()
    if not token:
        raise TokenNotConfigured()
    if urlparse(url).scheme != "https":
        raise InsecureTransportError(
            "Le jeton n'est transmis qu'en HTTPS : utiliser une BASE_URL en https://."
        )
    if not _same_origin(url, config.get_param("BASE_URL")):
        raise InsecureTransportError(
            f"Le jeton n'est transmis qu'à l'hôte configuré ({config.get_param('BASE_URL')})."
        )
    return {"Authorization": f"Token {token}"}


def _error_detail(response: requests.Response) -> str:
    """Extrait un message d'erreur lisible d'une réponse HTTP.

    Args:
        response: Réponse en erreur.

    Returns:
        Le champ ``detail`` de la réponse JSON s'il existe, sinon un extrait
        du corps de la réponse, sinon la raison HTTP.
    """
    try:
        payload = response.json()
    except ValueError:
        payload = None
    if isinstance(payload, dict) and payload.get("detail"):
        return str(payload["detail"])
    if payload:
        return str(payload)[:_MAX_DETAIL_LENGTH]
    text = (response.text or "").strip()
    return text[:_MAX_DETAIL_LENGTH] or (response.reason or "Erreur inconnue")


def get_api_response(
    url: str,
    params: Optional[Mapping[str, Any]] = None,
    use_token: bool = False,
) -> Any:
    """Exécute une requête GET et renvoie le contenu JSON décodé.

    Les nouvelles tentatives (erreurs réseau, codes 429 et 5xx) sont gérées par
    la session, avec une attente exponentielle bornée par ``MAX_ATTEMPTS``.

    Args:
        url: URL complète de la ressource.
        params: Paramètres de la requête (ajoutés à la chaîne de requête).
        use_token: ``True`` pour les endpoints à accès restreint.

    Returns:
        Le corps de la réponse décodé depuis le JSON.

    Raises:
        TokenNotConfigured: Si ``use_token`` est vrai sans jeton disponible.
        InsecureTransportError: Si le jeton devrait partir hors HTTPS ou vers
            un hôte non configuré.
        AuthenticationError: Si l'API répond 401 ou 403.
        ApiDFError: Pour tout autre code HTTP différent de 200, ou une réponse
            qui n'est pas du JSON.
        requests.RequestException: En cas d'URL invalide ou d'erreur réseau
            persistante.
    """
    headers = _auth_headers(url) if use_token else {}
    logger.debug("GET %s params=%s", url, dict(params) if params else {})
    response = get_session().get(
        url, params=params, headers=headers, timeout=config.get_param("TIMEOUT")
    )
    if response.status_code in (401, 403):
        raise AuthenticationError(response.status_code, _error_detail(response))
    if response.status_code != 200:
        raise ApiDFError(response.status_code, _error_detail(response))
    try:
        return response.json()
    except ValueError as exc:
        raise ApiDFError(response.status_code, "Réponse non JSON") from exc


def iter_pages(
    url: str,
    params: Optional[Mapping[str, Any]] = None,
    use_token: bool = False,
) -> Iterator[Tuple[List[Any], Optional[int]]]:
    """Parcourt toutes les pages d'une ressource paginée.

    Les pages suivantes sont lues à partir du lien ``next`` renvoyé par l'API,
    qui contient déjà l'ensemble des paramètres : ceux-ci ne sont donc pas
    renvoyés une seconde fois. Un lien ``next`` pointant vers un autre hôte
    que l'URL initiale est refusé.

    Args:
        url: URL de la première page.
        params: Paramètres de la première requête.
        use_token: ``True`` pour les endpoints à accès restreint.

    Yields:
        Des couples ``(enregistrements, total)`` où ``enregistrements`` est la
        liste ``results`` (ou ``features`` pour le GeoJSON) de la page et
        ``total`` le nombre total d'enregistrements annoncé par l'API.

    Raises:
        ApiFoncierError: Si un lien de pagination désigne un hôte inattendu.
    """
    next_url: Optional[str] = url
    next_params = params
    while next_url:
        payload = get_api_response(next_url, next_params, use_token=use_token)
        if isinstance(payload, list):
            yield payload, len(payload)
            return
        if not isinstance(payload, dict):
            raise ApiDFError(200, "Format de réponse inattendu")
        if "results" in payload:
            records = payload["results"]
        elif "features" in payload:
            records = payload["features"]
        else:
            yield [payload], 1
            return
        yield records, payload.get("count")
        candidate = payload.get("next")
        if candidate:
            if not _same_origin(candidate, url):
                raise ApiFoncierError(f"Lien de pagination inattendu : {candidate}")
            # Derrière un mandataire inverse, l'API peut produire des liens en
            # http:// : on conserve le schéma de la requête initiale.
            candidate = (
                urlparse(candidate)._replace(scheme=urlparse(url).scheme).geturl()
            )
        next_url, next_params = candidate, None

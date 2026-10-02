"""Configuration globale du module ``apifoncier``.

La configuration est un dictionnaire de paramètres partagé par toutes les
fonctions du module. Elle se modifie via :func:`configure` et se réinitialise
via :func:`reset`.

Paramètres disponibles :

==================  ===========================================  ==================================
Clé                 Rôle                                         Valeur par défaut
==================  ===========================================  ==================================
``BASE_URL``        URL racine de l'API                          ``https://apidf-preprod.cerema.fr``
``TOKEN``           Jeton d'accès aux données restreintes        ``None``
``PROXY``           URL du proxy HTTP(S)                         ``None``
``PROGRESS_BAR``    Affichage d'une barre de progression         ``True``
``MAX_ATTEMPTS``    Nombre maximal de tentatives par requête     ``3``
``BACKOFF_FACTOR``  Facteur d'attente exponentielle (secondes)   ``0.5``
``TIMEOUT``         Délai maximal d'attente d'une réponse (s)    ``15``
``PAGE_SIZE``       Nombre d'enregistrements par page            ``500``
``OUTPUT_FORMAT``   Format des tableaux : pandas ou polars       ``"pandas"``
``MAX_TILES``       Nombre maximal de tuiles par emprise         ``100``
``MAX_WORKERS``     Requêtes exécutées en parallèle              ``4``
``CACHE``           Cache HTTP local (extra ``cache``)           ``False``
``CACHE_EXPIRE``    Durée de validité du cache (s)               ``86400``
``CACHE_PATH``      Fichier SQLite du cache                      ``None`` (dossier de cache)
==================  ===========================================  ==================================

Les variables d'environnement ``APIFONCIER_TOKEN`` et ``APIFONCIER_BASE_URL``
sont prises en compte lorsque ``TOKEN`` et ``BASE_URL`` ne sont pas configurés
explicitement : elles évitent d'écrire le jeton en clair dans un script.
"""

from __future__ import annotations

import os
from typing import Any, Callable, Dict, Optional
from urllib.parse import urlparse

from .exceptions import ValidationError

ENV_TOKEN = "APIFONCIER_TOKEN"  # noqa: S105 (nom de variable)
ENV_BASE_URL = "APIFONCIER_BASE_URL"

OUTPUT_FORMATS = ("pandas", "polars")

CONFIG_INIT: Dict[str, Any] = {
    "BASE_URL": "https://apidf-preprod.cerema.fr",
    "TOKEN": None,
    "PROXY": None,
    "PROGRESS_BAR": True,
    "MAX_ATTEMPTS": 3,
    "BACKOFF_FACTOR": 0.5,
    "TIMEOUT": 15,
    "PAGE_SIZE": 500,
    "OUTPUT_FORMAT": "pandas",
    "MAX_TILES": 100,
    "MAX_WORKERS": 4,
    "CACHE": False,
    "CACHE_EXPIRE": 86400,
    "CACHE_PATH": None,
}


def _check_url(value: Any) -> str:
    """Vérifie qu'une valeur est une URL HTTP(S) absolue et retire le ``/`` final.

    Args:
        value: Valeur à contrôler.

    Returns:
        L'URL normalisée.

    Raises:
        ValidationError: Si la valeur n'est pas une URL HTTP(S) absolue.
    """
    parsed = urlparse(str(value))
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValidationError(f"URL invalide : {value!r} (http(s)://hote attendu).")
    return str(value).rstrip("/")


def _check_optional_url(value: Any) -> Optional[str]:
    """Contrôle une URL facultative (``None`` accepté).

    Args:
        value: Valeur à contrôler.

    Returns:
        L'URL normalisée ou ``None``.
    """
    return None if value is None else _check_url(value)


def _check_optional_str(value: Any) -> Optional[str]:
    """Contrôle une chaîne facultative non vide.

    Args:
        value: Valeur à contrôler.

    Returns:
        La chaîne débarrassée de ses espaces, ou ``None``.

    Raises:
        ValidationError: Si la valeur n'est ni ``None`` ni une chaîne non vide.
    """
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValidationError("Le jeton doit être une chaîne de caractères non vide.")
    return value.strip()


def _check_bool(value: Any) -> bool:
    """Contrôle un booléen.

    Args:
        value: Valeur à contrôler.

    Returns:
        Le booléen.

    Raises:
        ValidationError: Si la valeur n'est pas un booléen.
    """
    if not isinstance(value, bool):
        raise ValidationError(f"Booléen attendu, reçu {value!r}.")
    return value


def _check_positive_int(value: Any) -> int:
    """Contrôle un entier strictement positif.

    Args:
        value: Valeur à contrôler.

    Returns:
        L'entier.

    Raises:
        ValidationError: Si la valeur n'est pas un entier strictement positif.
    """
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValidationError(f"Entier strictement positif attendu, reçu {value!r}.")
    return value


def _check_positive_number(value: Any) -> float:
    """Contrôle un nombre positif ou nul.

    Args:
        value: Valeur à contrôler.

    Returns:
        Le nombre.

    Raises:
        ValidationError: Si la valeur n'est pas un nombre positif ou nul.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        raise ValidationError(f"Nombre positif attendu, reçu {value!r}.")
    return value


def _check_optional_path(value: Any) -> Optional[str]:
    """Contrôle un chemin de fichier facultatif.

    Args:
        value: Valeur à contrôler (chaîne, objet ``Path`` ou ``None``).

    Returns:
        Le chemin sous forme de chaîne, ou ``None``.

    Raises:
        ValidationError: Si la valeur est vide.
    """
    if value is None:
        return None
    path = str(value).strip()
    if not path:
        raise ValidationError("CACHE_PATH ne peut pas être vide.")
    return path


def _check_output_format(value: Any) -> str:
    """Contrôle le format de sortie des tableaux.

    Args:
        value: Valeur à contrôler.

    Returns:
        Le format en minuscules.

    Raises:
        ValidationError: Si le format n'est pas pris en charge.
    """
    fmt = str(value).lower()
    if fmt not in OUTPUT_FORMATS:
        raise ValidationError(
            f"OUTPUT_FORMAT doit valoir {' ou '.join(OUTPUT_FORMATS)}, reçu {value!r}."
        )
    return fmt


_VALIDATORS: Dict[str, Callable[[Any], Any]] = {
    "BASE_URL": _check_url,
    "TOKEN": _check_optional_str,
    "PROXY": _check_optional_url,
    "PROGRESS_BAR": _check_bool,
    "MAX_ATTEMPTS": _check_positive_int,
    "BACKOFF_FACTOR": _check_positive_number,
    "TIMEOUT": _check_positive_number,
    "PAGE_SIZE": _check_positive_int,
    "OUTPUT_FORMAT": _check_output_format,
    "MAX_TILES": _check_positive_int,
    "MAX_WORKERS": _check_positive_int,
    "CACHE": _check_bool,
    "CACHE_EXPIRE": _check_positive_int,
    "CACHE_PATH": _check_optional_path,
}


def _initial_config() -> Dict[str, Any]:
    """Construit la configuration initiale en tenant compte de l'environnement.

    Returns:
        Une copie de :data:`CONFIG_INIT`, avec ``BASE_URL`` surchargée par
        ``APIFONCIER_BASE_URL`` si cette variable est définie.
    """
    config = CONFIG_INIT.copy()
    env_base_url = os.environ.get(ENV_BASE_URL)
    if env_base_url:
        config["BASE_URL"] = _check_url(env_base_url)
    return config


CONFIG: Dict[str, Any] = _initial_config()

# Compteur incrémenté à chaque modification : il permet à la couche HTTP de
# savoir quand reconstruire sa session (proxy, nombre de tentatives, etc.).
_GENERATION = 0


def configure(**kwargs: Any) -> None:
    """Modifie la configuration globale du module.

    Les clés sont insensibles à la casse et contrôlées : une clé inconnue ou
    une valeur invalide lève une :class:`~apifoncier.exceptions.ValidationError`.

    Args:
        **kwargs: Paramètres à modifier (voir le tableau en tête de module).

    Raises:
        ValidationError: Si une clé est inconnue ou une valeur invalide.

    Examples:
        >>> import apifoncier
        >>> apifoncier.configure(TOKEN="mon_jeton", TIMEOUT=30)
        >>> apifoncier.configure(OUTPUT_FORMAT="polars")
    """
    global _GENERATION
    updates: Dict[str, Any] = {}
    for key, value in kwargs.items():
        upper = key.upper()
        if upper not in _VALIDATORS:
            raise ValidationError(
                f"Paramètre de configuration inconnu : {key!r}. "
                f"Paramètres disponibles : {', '.join(_VALIDATORS)}."
            )
        updates[upper] = _VALIDATORS[upper](value)
    CONFIG.update(updates)
    _GENERATION += 1


def get_param(value: str) -> Any:
    """Renvoie la valeur d'un paramètre de configuration.

    Args:
        value: Nom du paramètre (insensible à la casse).

    Returns:
        La valeur configurée, ou ``None`` si le paramètre n'existe pas.
    """
    return CONFIG.get(value.upper())


def get_token() -> Optional[str]:
    """Renvoie le jeton d'accès configuré, à défaut celui de l'environnement.

    Returns:
        Le jeton configuré via :func:`configure`, sinon la valeur de la
        variable d'environnement ``APIFONCIER_TOKEN``, sinon ``None``.
    """
    token = CONFIG.get("TOKEN")
    if token:
        return str(token)
    env_token = os.environ.get(ENV_TOKEN, "").strip()
    return env_token or None


def get_config() -> Dict[str, Any]:
    """Renvoie une copie de la configuration courante, jeton masqué.

    Returns:
        Un dictionnaire affichable sans risque de divulguer le jeton.
    """
    config = CONFIG.copy()
    if config.get("TOKEN"):
        config["TOKEN"] = "***"  # noqa: S105 (masquage)
    return config


def reset() -> None:
    """Réinitialise la configuration à ses valeurs par défaut."""
    global _GENERATION
    CONFIG.clear()
    CONFIG.update(_initial_config())
    _GENERATION += 1


def generation() -> int:
    """Renvoie le numéro de version courant de la configuration.

    Returns:
        Un entier incrémenté à chaque appel de :func:`configure` ou :func:`reset`.
    """
    return _GENERATION

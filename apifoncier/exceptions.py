"""Exceptions levées par le module ``apifoncier``.

Toutes les exceptions spécifiques au module héritent de :class:`ApiFoncierError`,
ce qui permet de les intercepter en un seul bloc ``except``.
"""

from __future__ import annotations

from typing import Optional


class ApiFoncierError(Exception):
    """Exception de base du module ``apifoncier``."""


class ValidationError(ApiFoncierError, ValueError):
    """Paramètre d'appel invalide, détecté avant toute requête réseau.

    Hérite de :class:`ValueError` pour rester compatible avec les versions
    antérieures du module, qui levaient directement cette exception.
    """


class ApiDFError(ApiFoncierError):
    """Erreur renvoyée par l'API Données foncières (code HTTP différent de 200).

    Attributes:
        status_code: Code HTTP renvoyé par l'API.
        detail: Message d'erreur extrait de la réponse.
    """

    def __init__(self, status_code: int, detail: Optional[str]) -> None:
        """Initialise l'exception.

        Args:
            status_code: Code HTTP renvoyé par l'API.
            detail: Message d'erreur extrait de la réponse.
        """
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Erreur {status_code} : {detail}")


class AuthenticationError(ApiDFError):
    """Jeton absent, invalide ou insuffisant pour la ressource demandée (401/403)."""


class TokenNotConfigured(ApiFoncierError):
    """Un endpoint à accès restreint est appelé sans jeton configuré."""

    def __init__(self) -> None:
        """Initialise l'exception avec un message d'aide."""
        super().__init__(
            "Le jeton n'a pas été configuré. Utiliser "
            'apifoncier.configure(TOKEN="jeton") ou définir la variable '
            "d'environnement APIFONCIER_TOKEN."
        )


class InsecureTransportError(ApiFoncierError):
    """Refus d'envoyer le jeton d'authentification sur une connexion non chiffrée."""

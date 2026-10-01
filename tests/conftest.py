"""Configuration commune des tests.

Par défaut, aucun test n'interroge l'API réelle : les réponses HTTP sont
simulées avec la bibliothèque ``responses``. Les tests marqués ``network``
ne s'exécutent qu'avec l'option ``--run-network``.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

import pytest

import apifoncier
import apifoncier.config

BASE_URL = "https://apidf-preprod.cerema.fr"
FAKE_TOKEN = "jeton-de-test"


def pytest_addoption(parser: pytest.Parser) -> None:
    """Ajoute l'option ``--run-network``."""
    parser.addoption(
        "--run-network",
        action="store_true",
        default=False,
        help="exécute les tests interrogeant l'API réelle",
    )


def pytest_collection_modifyitems(
    config: pytest.Config, items: List[pytest.Item]
) -> None:
    """Ignore les tests ``network`` sans l'option ``--run-network``."""
    if config.getoption("--run-network"):
        return
    skip = pytest.mark.skip(reason="activer avec --run-network")
    for item in items:
        if "network" in item.keywords:
            item.add_marker(skip)


@pytest.fixture(autouse=True)
def reset_config(monkeypatch: pytest.MonkeyPatch) -> None:
    """Réinitialise la configuration et neutralise l'environnement avant chaque test."""
    real = os.environ.get("APIFONCIER_TOKEN")
    if real:
        monkeypatch.setenv("APIFONCIER_TOKEN_REEL", real)
    monkeypatch.delenv("APIFONCIER_TOKEN", raising=False)
    monkeypatch.delenv("APIFONCIER_BASE_URL", raising=False)
    apifoncier.config.reset()
    apifoncier.configure(PROGRESS_BAR=False, BACKOFF_FACTOR=0)
    yield
    apifoncier.close_session()


@pytest.fixture
def token() -> str:
    """Configure un jeton fictif : les réponses étant simulées, aucun jeton réel n'est requis."""
    apifoncier.configure(TOKEN=FAKE_TOKEN)
    return FAKE_TOKEN


def page(
    results: List[Dict[str, Any]],
    next_url: Optional[str] = None,
    count: Optional[int] = None,
) -> Dict[str, Any]:
    """Construit une page de résultats au format de l'API."""
    return {
        "count": len(results) if count is None else count,
        "next": next_url,
        "previous": None,
        "results": results,
    }


def feature_page(
    features: List[Dict[str, Any]],
    next_url: Optional[str] = None,
    count: Optional[int] = None,
) -> Dict[str, Any]:
    """Construit une page GeoJSON au format de l'API."""
    return {
        "type": "FeatureCollection",
        "count": len(features) if count is None else count,
        "next": next_url,
        "previous": None,
        "features": features,
    }


def feature(
    identifier: str, lon: float, lat: float, **properties: Any
) -> Dict[str, Any]:
    """Construit une entité GeoJSON ponctuelle."""
    return {
        "type": "Feature",
        "id": identifier,
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
        "properties": properties,
    }

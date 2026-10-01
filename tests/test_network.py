"""Tests d'intégration interrogeant l'API réelle.

Ils ne s'exécutent qu'avec ``pytest --run-network``. Les tests sur les
endpoints à accès restreint sont en outre ignorés si la variable
d'environnement ``APIFONCIER_TOKEN`` n'est pas définie.
"""

import os

import pytest

import apifoncier
import apifoncier.cartofriches
import apifoncier.dvf_opendata
import apifoncier.ff
import apifoncier.ind_conso_espace
import apifoncier.utils

pytestmark = pytest.mark.network

needs_token = pytest.mark.skipif(
    not os.environ.get("APIFONCIER_TOKEN"), reason="APIFONCIER_TOKEN non défini"
)  # évalué à la collecte, avant la neutralisation de l'environnement


@pytest.fixture(autouse=True)
def real_token(monkeypatch):
    """Rétablit le jeton réel éventuellement défini dans l'environnement."""
    token = os.environ.get("APIFONCIER_TOKEN_REEL")
    if token:
        monkeypatch.setenv("APIFONCIER_TOKEN", token)


def test_friches_code_comm_correct_return_dataframe():
    df = apifoncier.cartofriches.friches(code_insee="59350")
    assert "site_id" in df.columns


def test_geofriches_returns_geodataframe():
    gdf = apifoncier.cartofriches.geofriches(code_insee="59350")
    assert gdf.crs == "EPSG:4326"


def test_dvf_opendata_bbox():
    df = apifoncier.dvf_opendata.mutations(in_bbox=[3.05, 50.62, 3.06, 50.63])
    assert "idmutation" in df.columns


def test_conso_espace_communes():
    df = apifoncier.ind_conso_espace.communes(code_insee="59350")
    assert not df.empty


def test_error_on_missing_parameter():
    with pytest.raises(apifoncier.ApiDFError):
        apifoncier.utils.get_api_response(
            f"{apifoncier.config.get_param('BASE_URL')}/cartofriches/friches/"
        )


@needs_token
def test_ff_parcelles_with_token():
    df = apifoncier.ff.parcelles(code_insee="59350", dcntpa_min=100000)
    assert "idpar" in df.columns

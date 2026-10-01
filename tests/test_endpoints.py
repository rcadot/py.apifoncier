"""Tests des fonctions publiques, sur réponses simulées.

Les endpoints à accès restreint (Fichiers fonciers, DV3F) sont testés avec un
jeton fictif : on vérifie la requête émise (chemin, paramètres, en-tête
d'authentification) et la mise en forme du résultat, sans accès réel.
"""

from urllib.parse import parse_qs, urlparse

import geopandas as gpd
import pandas as pd
import polars as pl
import pytest
import responses

import apifoncier
import apifoncier.cartofriches as cartofriches
import apifoncier.dv3f as dv3f
import apifoncier.dvf_opendata as dvf
import apifoncier.ff as ff
import apifoncier.ind_conso_espace as conso
import apifoncier.ind_marche as marche
import apifoncier.ind_prix as prix
from apifoncier.exceptions import TokenNotConfigured, ValidationError

from .conftest import BASE_URL, feature, feature_page, page

LIST_CASES = [
    # (fonction, kwargs, chemin attendu, paramètres attendus, jeton, geo)
    (
        cartofriches.friches,
        {"coddep": "59", "surface_min": 1000},
        "/cartofriches/friches/",
        {"coddep": "59", "surface_min": "1000"},
        False,
        False,
    ),
    (
        cartofriches.geofriches,
        {"in_bbox": [3, 50, 3.5, 50.5]},
        "/cartofriches/geofriches/",
        {"in_bbox": "3,50,3.5,50.5"},
        False,
        True,
    ),
    (
        dvf.mutations,
        {"code_insee": "59350", "segmtab": ["1", "2"]},
        "/dvf_opendata/mutations/",
        {"code_insee": "59350", "segmtab": "1,2"},
        False,
        False,
    ),
    (
        dvf.geomutations,
        {"code_insee": "59350", "anneemut_min": 2020},
        "/dvf_opendata/geomutations/",
        {"code_insee": "59350", "anneemut_min": "2020"},
        False,
        True,
    ),
    (
        dv3f.mutations,
        {"code_insee": "59350", "codtypproa": "P"},
        "/dv3f/mutations/",
        {"code_insee": "59350", "codtypproa": "P"},
        True,
        False,
    ),
    (
        dv3f.geomutations,
        {"code_insee": "59350", "filtre": "0"},
        "/dv3f/geomutations/",
        {"code_insee": "59350", "filtre": "0"},
        True,
        True,
    ),
    (
        ff.parcelles,
        {"code_insee": "59350", "jannatmin_min": 1950},
        "/ff/parcelles/",
        {"code_insee": "59350", "jannatmin_min": "1950"},
        True,
        False,
    ),
    (
        ff.geoparcelles,
        {"code_insee": "59350", "idpar": ["a1", "b2"]},
        "/ff/geoparcelles/",
        {"code_insee": "59350", "idpar": "a1,b2"},
        True,
        True,
    ),
    (
        ff.tups,
        {"code_insee": "59350", "typetup": "SIMPLE"},
        "/ff/tups/",
        {"code_insee": "59350", "typetup": "SIMPLE"},
        True,
        False,
    ),
    (
        ff.geotups,
        {"code_insee": "59350"},
        "/ff/geotups/",
        {"code_insee": "59350"},
        True,
        True,
    ),
    (
        ff.locaux,
        {"code_insee": "59350", "dteloc": ["1", "2"]},
        "/ff/locaux/",
        {"code_insee": "59350", "dteloc": "1,2"},
        True,
        False,
    ),
    (
        ff.proprios,
        {"code_insee": "59350", "typedroit": "P"},
        "/ff/proprios/",
        {"code_insee": "59350", "typedroit": "P"},
        True,
        False,
    ),
    (
        conso.communes,
        {"code_insee": "59350", "annee_min": 2015},
        "/indicateurs/conso_espace/communes/59350/",
        {"annee_min": "2015"},
        False,
        False,
    ),
    (
        conso.departements,
        {"coddep": "59"},
        "/indicateurs/conso_espace/departements/59/",
        {},
        False,
        False,
    ),
    (
        prix.aav,
        {"code_insee": "001", "periode": "triennal"},
        "/indicateurs/dv3f/aav/triennal/001/",
        {},
        False,
        False,
    ),
    (
        prix.communes,
        {"code_insee": "59350", "annee": 2020},
        "/indicateurs/dv3f/communes/annuel/59350/",
        {"annee": "2020"},
        False,
        False,
    ),
    (
        prix.departements,
        {"coddep": "59"},
        "/indicateurs/dv3f/departements/annuel/59/",
        {},
        False,
        False,
    ),
    (
        prix.epci,
        {"code_insee": "200093201"},
        "/indicateurs/dv3f/epci/annuel/200093201/",
        {},
        False,
        False,
    ),
    (
        prix.regions,
        {"code_insee": "32"},
        "/indicateurs/dv3f/regions/annuel/32/",
        {},
        False,
        False,
    ),
    (
        marche.prix_volume,
        {"echelle": "communes", "code": ["59350", "59009"]},
        "/indicateurs/dv3f/prix/annuel/",
        {"echelle": "communes", "code": "59350,59009"},
        False,
        False,
    ),
    (
        marche.activite,
        {"echelle": "aav", "code": "001"},
        "/indicateurs/dv3f/activite/",
        {"echelle": "aav", "code": "001"},
        False,
        False,
    ),
    (
        marche.accessibilite,
        {"code": "001", "annee": 2021},
        "/indicateurs/dv3f/accessibilite/",
        {"code": "001", "annee": "2021"},
        False,
        False,
    ),
    (
        marche.valorisation,
        {"echelle": "epci", "code_insee": "200093201"},
        "/indicateurs/dv3f/valorisation/epci/200093201/",
        {},
        False,
        False,
    ),
]


def _ids(case):
    return f"{case[0].__module__.split('.')[-1]}.{case[0].__name__}"


@pytest.mark.parametrize(
    "func,kwargs,path,expected,use_token,geo",
    LIST_CASES,
    ids=[_ids(c) for c in LIST_CASES],
)
@responses.activate
def test_list_endpoints(func, kwargs, path, expected, use_token, geo, token):
    body = feature_page([feature("id1", 3.0, 50.0, v=1)]) if geo else page([{"v": 1}])
    responses.get(f"{BASE_URL}{path}", json=body)

    result = func(**kwargs)

    request = responses.calls[0].request
    query = {k: v[0] for k, v in parse_qs(urlparse(request.url).query).items()}
    assert query.pop("page_size") == "500"
    assert query == expected
    assert ("Authorization" in request.headers) is use_token
    if geo:
        assert isinstance(result, gpd.GeoDataFrame)
        assert result.crs == "EPSG:4326"
        assert list(result.index) == ["id1"]
    else:
        assert isinstance(result, pd.DataFrame)
        assert list(result["v"]) == [1]


DETAIL_CASES = [
    (cartofriches.friche, "59350_12", "/cartofriches/friches/59350_12/", False),
    (dvf.mutation, 123, "/dvf_opendata/mutations/123/", False),
    (dv3f.mutation, "456", "/dv3f/mutations/456/", True),
    (ff.parcelle, "593500000A0001", "/ff/parcelles/593500000A0001/", True),
    (ff.tup, "uf593500000A0001", "/ff/tups/uf593500000A0001/", True),
    (ff.local, "593500123456", "/ff/locaux/593500123456/", True),
    (ff.proprio, "59350+00012", "/ff/proprios/59350%2B00012/", True),
]


@pytest.mark.parametrize(
    "func,identifier,path,use_token",
    DETAIL_CASES,
    ids=[c[0].__name__ for c in DETAIL_CASES],
)
@responses.activate
def test_detail_endpoints(func, identifier, path, use_token, token):
    responses.get(f"{BASE_URL}{path}", json={"id": str(identifier), "v": 1})
    df = func(identifier)
    assert len(df) == 1 and df["v"][0] == 1
    assert ("Authorization" in responses.calls[0].request.headers) is use_token


@pytest.mark.parametrize(
    "func,identifier,path,use_token",
    DETAIL_CASES,
    ids=[c[0].__name__ for c in DETAIL_CASES],
)
def test_detail_endpoints_reject_path_injection(
    func, identifier, path, use_token, token
):
    with pytest.raises(ValidationError):
        func("../../ff/proprios")


@pytest.mark.parametrize("func", [ff.parcelles, ff.locaux, dv3f.mutations])
def test_restricted_endpoints_require_token(func):
    with pytest.raises(TokenNotConfigured):
        func(code_insee="59350")


@responses.activate
def test_pagination_and_batching(token):
    url = f"{BASE_URL}/ff/parcelles/"
    next_url = f"{url}?code_insee=59001&page=2"
    codes = [f"{59001 + i}" for i in range(11)]
    responses.get(
        url,
        json=page([{"n": 1}], next_url=next_url, count=2),
        match=[
            responses.matchers.query_param_matcher(
                {"code_insee": ",".join(codes[:10]), "page_size": "500"}
            )
        ],
    )
    responses.get(next_url, json=page([{"n": 2}], count=2))
    responses.get(
        url,
        json=page([{"n": 3}]),
        match=[
            responses.matchers.query_param_matcher(
                {"code_insee": codes[10], "page_size": "500"}
            )
        ],
    )
    df = ff.parcelles(code_insee=codes)
    assert list(df["n"]) == [1, 2, 3]
    assert list(df.index) == [0, 1, 2]
    assert len(responses.calls) == 3


@responses.activate
def test_empty_geodataframe_has_crs():
    responses.get(f"{BASE_URL}/cartofriches/geofriches/", json=feature_page([]))
    gdf = cartofriches.geofriches(code_insee="59350")
    assert gdf.empty and gdf.crs == "EPSG:4326"


@responses.activate
def test_polars_output():
    apifoncier.configure(OUTPUT_FORMAT="polars")
    responses.get(
        f"{BASE_URL}/dvf_opendata/mutations/", json=page([{"v": 1}, {"v": 2}])
    )
    df = dvf.mutations(code_insee="59350")
    assert isinstance(df, pl.DataFrame)
    assert df["v"].to_list() == [1, 2]


@responses.activate
def test_page_size_configuration():
    apifoncier.configure(PAGE_SIZE=100)
    responses.get(f"{BASE_URL}/dvf_opendata/mutations/", json=page([]))
    dvf.mutations(code_insee="59350")
    assert "page_size=100" in responses.calls[0].request.url


@responses.activate
def test_deprecated_jannathmin_is_renamed(token):
    responses.get(f"{BASE_URL}/ff/parcelles/", json=page([]))
    with pytest.warns(DeprecationWarning, match="jannatmin_min"):
        ff.parcelles(code_insee="59350", jannathmin_min=1950)
    query = parse_qs(urlparse(responses.calls[0].request.url).query)
    assert query["jannatmin_min"] == ["1950"]
    assert "jannathmin_min" not in query


@responses.activate
def test_lon_lat_query():
    responses.get(f"{BASE_URL}/cartofriches/friches/", json=page([]))
    cartofriches.friches(lon_lat=[3.0, 50.0])
    query = parse_qs(urlparse(responses.calls[0].request.url).query)
    assert query["contains_geom"] == ['{"type": "Point", "coordinates": [3.0, 50.0]}']


def test_bbox_limits():
    with pytest.raises(ValidationError, match=r"0\.02"):
        dvf.mutations(in_bbox=[3, 50, 3.1, 50.1])


@pytest.mark.parametrize(
    "call",
    [
        lambda: prix.communes(code_insee="59350", periode="mensuel"),
        lambda: marche.prix_volume(echelle="pays", code="FR"),
        lambda: marche.prix_volume(echelle="communes", code="59350", periode="x"),
        lambda: marche.activite(code="59350"),
        lambda: marche.valorisation(echelle="communes", code_insee="59350"),
        lambda: conso.communes(),
    ],
)
def test_invalid_indicator_arguments(call):
    with pytest.raises(ValueError):
        call()


@responses.activate
def test_generic_get():
    responses.get(f"{BASE_URL}/cartofriches/friches/", json=page([{"v": 1}]))
    df = apifoncier.get("/cartofriches/friches", code_insee="59350")
    assert list(df["v"]) == [1]


@responses.activate
def test_generic_get_without_location():
    responses.get(f"{BASE_URL}/autre/endpoint/", json=page([{"v": 1}]))
    assert len(apifoncier.get("/autre/endpoint/", annee=2020)) == 1


@pytest.mark.parametrize(
    "endpoint", ["ff/parcelles/", "/ff/../x/", "/ff/parcelles/?a=1", "https://x.org/"]
)
def test_generic_get_rejects_invalid_endpoints(endpoint):
    with pytest.raises(ValidationError):
        apifoncier.get(endpoint)

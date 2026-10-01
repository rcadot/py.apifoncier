import pytest
import responses
from requests.exceptions import MissingSchema

import apifoncier.utils
from apifoncier import exceptions

from .conftest import BASE_URL, feature, feature_page, page


def test_get_api_response_raise_exception_with_incorrect_url():
    url = "toto"
    with pytest.raises(MissingSchema):
        apifoncier.utils.get_api_response(url)


@responses.activate
def test_get_api_response_works_with_correct_url():
    url = f"{BASE_URL}/cartofriches/friches/"
    responses.get(url, json=page([{"site_id": "1"}]))
    response = apifoncier.utils.get_api_response(url, {"code_insee": "59350"})
    assert isinstance(response, dict)
    assert "results" in response


@responses.activate
def test_get_api_response_with_missing_param_send_exception():
    url = f"{BASE_URL}/cartofriches/friches/"
    responses.get(url, status=400, json={"detail": "Paramètre manquant"})
    with pytest.raises(exceptions.ApiDFError) as e:
        apifoncier.utils.get_api_response(url)
    assert e.value.status_code == 400
    assert "Paramètre manquant" in str(e.value)


def test_get_api_response_with_use_token_true_but_no_token_given():
    url = "http://test-api.net"
    with pytest.raises(exceptions.TokenNotConfigured):
        apifoncier.utils.get_api_response(url, use_token=True)


@responses.activate
def test_get_all_data_and_geodata():
    url = f"{BASE_URL}/x/"
    responses.get(url, json=page([{"a": 1}, {"a": 2}]))
    assert list(apifoncier.utils.get_all_data(url)["a"]) == [1, 2]
    responses.replace(responses.GET, url, json=feature_page([feature("f1", 3, 50)]))
    gdf = apifoncier.utils.get_all_geodata(url)
    assert list(gdf.index) == ["f1"]


@responses.activate
def test_resultat_compatibility():
    url = f"{BASE_URL}/cartofriches/friches/"
    responses.get(url, json=page([{"site_id": "1"}]))
    df = apifoncier.utils.Resultat(
        "/cartofriches/friches/", code_insee="59350"
    ).get_dataframe()
    assert list(df["site_id"]) == ["1"]


def test_is_num():
    assert apifoncier.utils.is_num(1)
    assert apifoncier.utils.is_num(1.5)
    assert not apifoncier.utils.is_num(True)
    assert not apifoncier.utils.is_num("1")
    assert not apifoncier.utils.is_num(float("nan"))

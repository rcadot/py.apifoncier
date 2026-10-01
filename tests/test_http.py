from urllib.parse import parse_qs, urlparse

import pytest
import requests
import responses

import apifoncier
from apifoncier import _http
from apifoncier.exceptions import (
    ApiDFError,
    ApiFoncierError,
    AuthenticationError,
    InsecureTransportError,
    TokenNotConfigured,
)

from .conftest import BASE_URL, page

URL = f"{BASE_URL}/ff/parcelles/"


@responses.activate
def test_retry_on_server_error_then_success():
    responses.get(URL, status=503)
    responses.get(URL, json=page([{"idpar": "1"}]))
    assert _http.get_api_response(URL)["results"] == [{"idpar": "1"}]
    assert len(responses.calls) == 2


@responses.activate
def test_retries_are_bounded_by_max_attempts():
    apifoncier.configure(MAX_ATTEMPTS=2)
    responses.get(URL, status=502, body="Bad gateway")
    with pytest.raises(ApiDFError) as exc:
        _http.get_api_response(URL)
    assert exc.value.status_code == 502
    assert len(responses.calls) == 2


@responses.activate
def test_no_retry_on_client_error():
    responses.get(URL, status=404, json={"detail": "Pas trouvé."})
    with pytest.raises(ApiDFError, match="Pas trouvé"):
        _http.get_api_response(URL)
    assert len(responses.calls) == 1


@responses.activate
def test_error_without_json_body():
    responses.get(URL, status=400, body="<html>erreur</html>")
    with pytest.raises(ApiDFError, match="erreur"):
        _http.get_api_response(URL)


@responses.activate
@pytest.mark.parametrize("status", [401, 403])
def test_authentication_errors(status, token):
    responses.get(URL, status=status, json={"detail": "Jeton invalide."})
    with pytest.raises(AuthenticationError) as exc:
        _http.get_api_response(URL, use_token=True)
    assert exc.value.status_code == status
    assert isinstance(exc.value, ApiDFError)


@responses.activate
def test_non_json_success_response():
    responses.get(URL, body="pas du json")
    with pytest.raises(ApiDFError, match="non JSON"):
        _http.get_api_response(URL)


@responses.activate
def test_token_header_only_when_requested(token):
    responses.get(URL, json=page([]))
    _http.get_api_response(URL)
    assert "Authorization" not in responses.calls[0].request.headers
    _http.get_api_response(URL, use_token=True)
    assert responses.calls[1].request.headers["Authorization"] == f"Token {token}"


@responses.activate
def test_user_agent_header():
    responses.get(URL, json=page([]))
    _http.get_api_response(URL)
    agent = responses.calls[0].request.headers["User-Agent"]
    assert agent == f"apifoncier-python/{apifoncier.__version__}"


def test_token_from_environment_is_used(monkeypatch):
    monkeypatch.setenv("APIFONCIER_TOKEN", "jeton-env")
    assert _http._auth_headers(URL) == {"Authorization": "Token jeton-env"}


def test_missing_token():
    with pytest.raises(TokenNotConfigured):
        _http.get_api_response(URL, use_token=True)


def test_token_never_sent_over_http(token):
    apifoncier.configure(BASE_URL="http://apidf-preprod.cerema.fr")
    with pytest.raises(InsecureTransportError):
        _http.get_api_response(
            "http://apidf-preprod.cerema.fr/ff/parcelles/", use_token=True
        )


def test_token_never_sent_to_another_host(token):
    with pytest.raises(InsecureTransportError):
        _http.get_api_response("https://exemple.org/ff/parcelles/", use_token=True)


@responses.activate
def test_iter_pages_follows_next_without_duplicating_params():
    next_url = f"{URL}?code_insee=59350&page=2&page_size=1"
    responses.get(URL, json=page([{"n": 1}], next_url=next_url, count=2))
    responses.get(next_url, json=page([{"n": 2}], count=2))
    pages = list(_http.iter_pages(URL, {"code_insee": "59350", "page_size": 1}))
    assert [records for records, _ in pages] == [[{"n": 1}], [{"n": 2}]]
    second = parse_qs(urlparse(responses.calls[1].request.url).query)
    assert second["code_insee"] == ["59350"]


@responses.activate
def test_iter_pages_refuses_foreign_next_link():
    responses.get(URL, json=page([{"n": 1}], next_url="https://pirate.example/?page=2"))
    with pytest.raises(ApiFoncierError, match="inattendu"):
        list(_http.iter_pages(URL))


@responses.activate
def test_iter_pages_upgrades_http_next_link(token):
    http_next = "http://apidf-preprod.cerema.fr/ff/parcelles/?page=2"
    responses.get(URL, json=page([{"n": 1}], next_url=http_next, count=2))
    responses.get(f"{URL}?page=2", json=page([{"n": 2}], count=2))
    pages = list(_http.iter_pages(URL, use_token=True))
    assert len(pages) == 2
    assert responses.calls[1].request.url.startswith("https://")


def test_session_is_reused_and_rebuilt_on_configure():
    first = _http.get_session()
    assert _http.get_session() is first
    apifoncier.configure(PROXY="http://proxy.local:3128")
    second = _http.get_session()
    assert second is not first
    assert second.proxies["https"] == "http://proxy.local:3128"


@responses.activate
def test_connection_error_is_raised_after_retries():
    apifoncier.configure(MAX_ATTEMPTS=2)
    responses.get(URL, body=requests.ConnectionError("réseau indisponible"))
    with pytest.raises(requests.ConnectionError):
        _http.get_api_response(URL)

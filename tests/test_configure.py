import pytest

import apifoncier
import apifoncier.config
from apifoncier.exceptions import ValidationError


def test_default_token_config_is_none():
    assert apifoncier.config.get_param("TOKEN") is None


def test_default_proxy_config_is_none():
    assert apifoncier.config.get_param("PROXY") is None


def test_default_base_url_config_is_preprod_url():
    base_url = "https://apidf-preprod.cerema.fr"
    assert apifoncier.config.get_param("BASE_URL") == base_url


def test_change_token_config_ok():
    token_value = "mon_token"
    apifoncier.configure(TOKEN=token_value)
    TOKEN = apifoncier.config.get_param("TOKEN")
    assert TOKEN == token_value


def test_change_proxy_config_ok():
    proxy_value = "http://mon.proxy.net:8080"
    apifoncier.configure(PROXY=proxy_value)
    PROXY = apifoncier.config.get_param("PROXY")
    assert PROXY == proxy_value


def test_change_base_url_config_ok():
    new_url = "https://toto.net"
    apifoncier.configure(BASE_URL=new_url)
    BASE_URL = apifoncier.config.get_param("BASE_URL")
    assert BASE_URL == new_url


def test_reset_works():
    apifoncier.configure(TOKEN="mon_token", BASE_URL="https://toto.net")

    apifoncier.config.reset()
    BASE_URL = apifoncier.config.get_param("BASE_URL")
    assert BASE_URL == "https://apidf-preprod.cerema.fr"
    TOKEN = apifoncier.config.get_param("TOKEN")
    assert TOKEN is None


def test_keys_are_case_insensitive():
    apifoncier.configure(timeout=30)
    assert apifoncier.config.get_param("TIMEOUT") == 30


def test_base_url_trailing_slash_is_removed():
    apifoncier.configure(BASE_URL="https://toto.net/")
    assert apifoncier.config.get_param("BASE_URL") == "https://toto.net"


@pytest.mark.parametrize(
    "kwargs",
    [
        {"UNKNOWN": 1},
        {"BASE_URL": "toto.net"},
        {"MAX_ATTEMPTS": 0},
        {"TIMEOUT": -1},
        {"PAGE_SIZE": "500"},
        {"PROGRESS_BAR": "oui"},
        {"OUTPUT_FORMAT": "arrow"},
        {"TOKEN": ""},
    ],
)
def test_invalid_configuration_is_rejected(kwargs):
    with pytest.raises(ValidationError):
        apifoncier.configure(**kwargs)


def test_invalid_configuration_is_also_a_value_error():
    with pytest.raises(ValueError):
        apifoncier.configure(MAX_ATTEMPTS=0)


def test_token_from_environment(monkeypatch):
    monkeypatch.setenv("APIFONCIER_TOKEN", "jeton-env")
    assert apifoncier.config.get_token() == "jeton-env"


def test_configured_token_has_priority_over_environment(monkeypatch):
    monkeypatch.setenv("APIFONCIER_TOKEN", "jeton-env")
    apifoncier.configure(TOKEN="jeton-config")
    assert apifoncier.config.get_token() == "jeton-config"


def test_base_url_from_environment(monkeypatch):
    monkeypatch.setenv("APIFONCIER_BASE_URL", "https://autre.api.fr/")
    apifoncier.config.reset()
    assert apifoncier.config.get_param("BASE_URL") == "https://autre.api.fr"


def test_get_config_masks_token():
    apifoncier.configure(TOKEN="secret")
    assert apifoncier.get_config()["TOKEN"] == "***"
    assert apifoncier.config.get_param("TOKEN") == "secret"

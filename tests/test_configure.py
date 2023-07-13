import pytest
import apifoncier
import apifoncier.config


@pytest.fixture(autouse=True)
def reset_config():
    """
    Fixture pour réinitialiser la conf avant chaque test.
    """
    apifoncier.config.reset()


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
    apifoncier.configure(TOKEN="mon_token", BASE_URL="toto.net")

    apifoncier.config.reset()
    BASE_URL = apifoncier.config.get_param("BASE_URL")
    assert BASE_URL == "https://apidf-preprod.cerema.fr"
    TOKEN = apifoncier.config.get_param("TOKEN")
    assert TOKEN is None

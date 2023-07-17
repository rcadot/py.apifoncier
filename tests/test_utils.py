import pytest
import warnings

import apifoncier.utils

from requests.exceptions import MissingSchema
from apifoncier import exceptions


@pytest.fixture(autouse=True)
def reset_config():
    """
    Fixture pour réinitialiser la conf avant chaque test.
    """
    apifoncier.config.reset()


def test_get_api_response_raise_exception_with_incorrect_url():
    url = "toto"
    with pytest.raises(MissingSchema):
        response = apifoncier.utils.get_api_response(url)


def test_get_api_response_works_with_correct_url():
    url = "https://apidf-preprod.cerema.fr/cartofriches/friches/?code_insee=59350"
    response = apifoncier.utils.get_api_response(url)
    assert isinstance(response, dict)
    assert "results" in response


def test_get_api_response_with_missing_param_send_exception():
    url = "https://apidf-preprod.cerema.fr/cartofriches/friches/"
    with pytest.raises(exceptions.ApiDFError) as e:
        response = apifoncier.utils.get_api_response(url)


def test_get_api_response_with_use_token_true_but_no_token_given():
    url = "http://test-api.net"
    with pytest.raises(exceptions.TokenNotConfigured):
        response = apifoncier.utils.get_api_response(url, use_token=True)

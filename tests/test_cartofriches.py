import pytest
import apifoncier.cartofriches


@pytest.fixture(autouse=True)
def reset_config():
    """
    Fixture pour réinitialiser la conf avant chaque test.
    """
    apifoncier.config.reset()


def test_friches_code_comm_correct_return_dataframe():
    df = apifoncier.cartofriches.friches(code_insee="59350")
    assert "site_id" in df.columns

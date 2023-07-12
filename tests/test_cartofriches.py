import pytest
import apifoncier


def test_friches_code_comm_correct_return_dataframe():
    df = apifoncier.cartofriches.friches(code_insee="59350")
    assert "site_id" in df.columns

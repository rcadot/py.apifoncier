import json

import pytest

from apifoncier import _query
from apifoncier.exceptions import ValidationError


def plan(params, **kwargs):
    return _query.build_requests("/ep/", dict(params), **kwargs)


def test_codes_insee_are_batched_by_ten():
    codes = [str(59000 + i) for i in range(12)]
    requests_ = plan({"code_insee": codes, "fields": "all"})
    assert [p["code_insee"] for _, p in requests_] == [
        ",".join(codes[:10]),
        ",".join(codes[10:]),
    ]
    assert all(p["fields"] == "all" for _, p in requests_)


def test_single_code_as_string_or_int():
    assert plan({"code_insee": "59350"}) == [("/ep/", {"code_insee": "59350"})]
    assert plan({"code_insee": 59350}) == [("/ep/", {"code_insee": "59350"})]


def test_coddep_one_request_per_code():
    assert [p["coddep"] for _, p in plan({"coddep": ["59", "62"]})] == ["59", "62"]


def test_path_code():
    requests_ = plan({"code_insee": ["59350", "2A004"], "annee": 2020}, path_code=True)
    assert requests_ == [
        ("/ep/59350/", {"annee": 2020}),
        ("/ep/2A004/", {"annee": 2020}),
    ]


def test_lon_lat_builds_bbox_and_geojson_point():
    ((_, params),) = plan({"lon_lat": [3.0, 50.0]})
    assert params["in_bbox"] == "2.99,49.99,3.01,50.01"
    assert json.loads(params["contains_geom"]) == {
        "type": "Point",
        "coordinates": [3.0, 50.0],
    }


def test_in_bbox_serialised():
    ((_, params),) = plan({"in_bbox": [3, 50, 3.01, 50.01]})
    assert params["in_bbox"] == "3,50,3.01,50.01"


@pytest.mark.parametrize(
    "bbox",
    [
        [3, 50, 3.01],
        [3, 50, "a", 51],
        [3.01, 50, 3, 50.01],
        [3, 50, 3.5, 50.5],
        [200, 0, 201, 0.01],
    ],
)
def test_invalid_bbox(bbox):
    with pytest.raises(ValidationError):
        plan({"in_bbox": bbox})


def test_bbox_limit_can_be_widened_or_disabled():
    assert plan({"in_bbox": [3, 50, 3.5, 50.5]}, max_bbox=1.0)
    assert plan({"in_bbox": [3, 50, 5, 52]}, max_bbox=None)


@pytest.mark.parametrize("value", [[3.0], "3,50", [3.0, 95.0], [True, 50.0]])
def test_invalid_lon_lat(value):
    with pytest.raises(ValidationError):
        plan({"lon_lat": value})


def test_missing_location_raises():
    with pytest.raises(ValidationError, match="au moins un paramètre"):
        plan({"fields": "all"})


def test_missing_location_allowed_when_not_required():
    assert plan({"fields": "all"}, location_required=False) == [
        ("/ep/", {"fields": "all"})
    ]


def test_several_locations_warn_and_use_priority():
    with pytest.warns(UserWarning, match="Seul le mot-clé in_bbox"):
        requests_ = plan({"code_insee": "59350", "in_bbox": [3, 50, 3.01, 50.01]})
    assert "code_insee" not in requests_[0][1]


@pytest.mark.parametrize("code", ["../ff", "59350/", "59 350", "", "59350?x=1", "a%2F"])
def test_codes_with_unsafe_characters_are_rejected(code):
    with pytest.raises(ValidationError):
        plan({"code_insee": [code]}, path_code=True)


def test_empty_code_list_rejected():
    with pytest.raises(ValidationError):
        plan({"code_insee": []})


def test_path_segment_accepts_ff_identifiers():
    assert _query.path_segment("590001+00123", "idprocpte") == "590001%2B00123"
    with pytest.raises(ValidationError):
        _query.path_segment(None, "idpar")


def test_clean_params():
    assert _query.clean_params({"a": None, "b": ["1", " 2"], "c": True, "d": 3}) == {
        "b": "1,2",
        "c": "true",
        "d": 3,
    }

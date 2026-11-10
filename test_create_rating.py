import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"

# Base choice: 3 stars as a whole number, a real pizza, the user's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id

# C1: stars below 1 or above 5
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}

# C2: non-integer stars or missing field
@pytest.mark.parametrize("stars", [3.5, "3"])
def test_stars_invalid_type(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400

def test_stars_missing_field(api, auth, pizza_id):
    new = {"pizza_id": pizza_id}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code == 400

# C3: pizza does not exist
def test_pizza_does_not_exist(api, auth):
    new = {"pizza_id": 999999999, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)
    assert res.status_code in [400, 404]

# C4: missing or invalid authorization header
def test_rating_no_token(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new)
    assert res.status_code == 401

def test_rating_invalid_token(api, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    invalid_auth = {"Authorization": "token short"}
    res = api.post("/api/ratings", json=new, headers=invalid_auth)
    assert res.status_code == 401
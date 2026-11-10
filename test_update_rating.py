import pytest

# Boundary values for updating stars: 1 and 5 succeed, 0 and 6 are refused.
@pytest.mark.parametrize("stars, expected_status", [(1, 200), (5, 200), (0, 400), (6, 400)])
def test_update_rating_boundary_values(api, auth, rating, stars, expected_status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected_status
    
    # Verify rating stars state
    get_res = api.get(path, headers=auth)
    if expected_status == 200:
        assert get_res.json()["stars"] == stars
    else:
        assert get_res.json()["stars"] == 3  # Original value kept
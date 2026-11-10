# A user must not read, update or delete another user's rating.
def test_other_user_cannot_read_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.get(path, headers=other_auth)
    assert 400 <= res.status_code <= 499
    
    # Confirm owner still has the rating
    owner_res = api.get(path, headers=auth)
    assert owner_res.status_code == 200

def test_other_user_cannot_update_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": 5}, headers=other_auth)
    assert 400 <= res.status_code <= 499
    
    # Confirm rating was unchanged
    owner_res = api.get(path, headers=auth)
    assert owner_res.json()["stars"] == 3

def test_other_user_cannot_delete_rating(api, auth, other_auth, rating):
    path = f"/api/ratings/{rating['id']}"
    res = api.delete(path, headers=other_auth)
    assert 400 <= res.status_code <= 499
    
    # Confirm rating still exists
    owner_res = api.get(path, headers=auth)
    assert owner_res.status_code == 200
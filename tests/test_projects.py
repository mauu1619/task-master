def test_project_ownership(client):
    client.post("/api/users/", json={"username": "owner", "password": "pass", "email": "o@m.co"})
    token = client.post("/api/login/token", data={"username": "owner", "password": "pass"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj_resp = client.post("/api/projects/", json={"title": "Test Proj"}, headers=headers)
    assert proj_resp.status_code == 200
    assert proj_resp.json()["owner_id"] is not None


def test_access_denied_for_other_user(client):
    client.post("/api/user/registration", json={"username": "u1", "password": "p1", "email": "1@m.co"})
    t1 = client.post("/api/login/token", data={"username": "u1", "password": "p1"}).json()["access_token"]
    p1_id = client.post("/api/projects/", json={"title": "P1"}, headers={"Authorization": f"Bearer {t1}"}).json()["id"]

    client.post("/api/user/registration", json={"username": "u2", "password": "p2", "email": "2@m.co"})
    t2 = client.post("/api/login/token", data={"username": "u2", "password": "p2"}).json()["access_token"]

    delete_resp = client.delete(f"/api/projects/{p1_id}", headers={"Authorization": f"Bearer {t2}"})
    
    assert delete_resp.status_code == 403
    assert delete_resp.json()["detail"] == "Not enough permissions"
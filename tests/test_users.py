def test_user_flow(client):
    user_data = {"username": "daniil_test", "password": "securepassword", "email": "test@mail.com"}
    reg_resp = client.post("/api/user/registration", json=user_data)
    assert reg_resp.status_code == 200
    
    login_data = {"username": "daniil_test", "password": "securepassword"}
    login_resp = client.post("/api/login/token", data=login_data)
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()
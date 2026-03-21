def test_register(client):
    response = client.post(
        "api/user/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data['username'] == 'newuser'
    assert data['email'] == 'newuser@example.com'
    assert 'password' not in data


def test_register_duplicate_username(client, test_user):
    response = client.post(
        "api/user/register",
        json={
            'username': 'testuser',
            'password': 'testuser123'
        }
    )
    assert response.status_code == 400
    assert "User already exists" in response.json()['detail']


def test_login_success(client, test_user):
    response = client.post(
        "api/login/token",
        data={
            'username': 'testuser',
            'password': 'testuser123'
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert data['token_type'] == 'bearer'


def test_login_wrong_password(client, test_user):
    response = client.post(
        'api/login/token',
        data={
            'username': 'testuser',
            'password': 'testuser456'
        }
    )
    assert response.status_code == 401
    assert "Incorrect username or password" == response.json()["detail"]


def test_login_nonexistent_user(client):
    response = client.post(
        'api/login/token',
        data={
            'username': 'somebody',
            'password': 'password'
        }
    )
    assert response.status_code == 401
    assert "Incorrect username or password" == response.json()["detail"]
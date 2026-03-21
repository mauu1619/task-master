def test_no_projects(client, user_token):
    response = client.get("api/projects/", headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert response.status_code == 200
    assert "There are no projects yet" == response.json()['message']


def test_create_and_count_projects(client, test_project, user_token):
    create_response = client.post(
        "api/projects/",
        json={
            'title': 'newproject',
            'description': 'this is a new project'
        },
        headers={"Authorization": f'Bearer {user_token}'}
    )
    assert create_response.status_code == 201

    check_response = client.get("api/projects/", headers={
        "Authorization": f"Bearer {user_token}"
    })
    assert check_response.status_code == 200
    
    data = check_response.json()
    assert len(data) == 2

    titles = [p['title'] for p in data]
    assert 'newproject' in titles
    assert 'testproject' in titles
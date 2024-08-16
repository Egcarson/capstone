import pytest


@pytest.mark.parametrize("username, email, password", [("user1", "user1@gmail.com", "user1")])
def test_get_users(client, setup_database, username, email, password):

    # creating a user for testing purposes
    response = client.post(
        "/signup",
        json={"username": username, "email": email, "password": password},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == username

    # getting a user
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    response_data = data[0]
    assert response_data["username"] == username


@pytest.mark.parametrize("username", [("user1")])
def test_get_user_by_username(client, setup_database, username):

    fake_username = "user2"
    # test for error code (404 - user not found)
    response = client.get(f"/users/username/{fake_username}")
    assert response.status_code == 404

    # main test
    response = client.get(f"/users/username/{username}")
    assert response.status_code == 200
    data = response.json()
    assert data['username'] == username


@pytest.mark.parametrize("username", [("user1")])
def test_get_user_by_id(client, setup_database, username):

    # test for error code (404 - user not found)
    response = client.get("/users/3")
    assert response.status_code == 404

    # main test
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data['username'] == username


@pytest.mark.parametrize("username, email", [("user2", "user2@gmail.com")])
def test_update_user(client, setup_database, username, email):

    user_payload = {"username": username, "email": email}
    # test for error code (404 - user not found)
    response = client.put("/users/3", json=user_payload)
    assert response.status_code == 404

    # main test
    response = client.put("/users/1", json=user_payload)
    assert response.status_code == 202
    data = response.json()
    assert data['username'] == username


@pytest.mark.parametrize("username, email", [("user2", "user2@gmail.com")])
def test_delete_user(client, setup_database, username, email):

    # test for error code (404 - user not found)
    response = client.delete("/users/3")
    assert response.status_code == 404

    # main test
    response = client.delete("/users/1")
    assert response.status_code == 204

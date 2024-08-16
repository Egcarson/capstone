import pytest

# test for signing up a user


@pytest.mark.parametrize("username, email, password", [("testuser", "test@gmail.com", "test1")])
def test_signup(client, setup_database, username, email, password):

    # main test
    response = client.post(
        "/signup",
        json={"username": username, "email": email, "password": password},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == username
    assert data["email"] == email

    # asserting error (406 - user already exists)
    response = client.post(
        "/signup",
        json={"username": username, "email": email, "password": password},
    )
    assert response.status_code == 406

# test for logging in a user


@pytest.mark.parametrize("username, password", [("testuser", "test1")])
def test_login(client, setup_database, username, password):
    fake_username = "testuser1"
    fake_password = "password"

    # asserting error (401 - username or password incorrect)
    response = client.post(
        "/login",
        data={"username": fake_username, "password": fake_password},
    )
    assert response.status_code == 401

    # logging the new user for testing
    response = client.post(
        "/login",
        data={"username": username, "password": password},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"

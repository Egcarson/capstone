def test_add_movie(client, setup_database, auth_headers):

    movie_title = "testing movie title"
    movie_data = {"title": movie_title, "genre": "Drama"}

    # assertion for error (403)
    response = client.post(
        f"/movies"
    )
    assert response.status_code == 401

    # test for adding a movie
    response = client.post(
        "/movies",
        json=movie_data, headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == movie_title

    # assertion for error (400)
    response = client.post(
        "/movies",
        json=movie_data, headers=auth_headers
    )

    assert response.status_code == 400


def test_get_movies(client, setup_database, auth_headers):
    movie_title = "testing movie title"
    response = client.get(
        "/movies?skip=0&limit=10", headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    response_data = data[0]
    assert response_data["title"] == movie_title


def test_get_movie(client, setup_database, auth_headers):

    movie_title = "testing movie title"

    # asserting for error(404)
    response = client.get(
        "/movies/{title}", headers=auth_headers
    )
    assert response.status_code == 404

    # assertion for getting a movie
    response = client.get(
        f"/movies/{movie_title}", headers=auth_headers
    )
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == movie_title


def test_update_movie(client, setup_database, auth_headers):

    movie_title = "testing movie title"
    new_title = "updated movie title"
    movie_data = {"title": new_title, "genre": "Drama"}

    # asserting for error(404)
    response = client.put(
        f"/movies/{new_title}", json=movie_data, headers=auth_headers
    )
    assert response.status_code == 404

    # assertion for error (401)
    response = client.put(
        f"/movies/{movie_title}", json=movie_data
    )
    assert response.status_code == 401

    # assertion for updating movie
    response = client.put(
        f"/movies/{movie_title}",
        json=movie_data, headers=auth_headers
    )

    assert response.status_code == 202
    data = response.json()
    assert data["title"] == new_title


def test_delete_movie(client, setup_database, auth_headers):

    movie_title = "updated movie title"
    bang = "bang"
    # asserting for error(404)
    response = client.delete(
        f"/movies/{bang}", headers=auth_headers
    )
    assert response.status_code == 404

    # assertion for error (401)
    response = client.delete(
        f"/movies/{movie_title}"
    )
    assert response.status_code == 401

    # assertion for delete_movie
    response = client.delete(
        f"/movies/{movie_title}", headers=auth_headers
    )

    assert response.status_code == 204

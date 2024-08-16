def test_add_rate(client, setup_database, auth_headers):
    # add a movie with the title for rating
    movie_title = "rate_movie"
    movie_data = {"title": movie_title, "genre": "Drama"}
    response = client.post(
        "/movies",
        json=movie_data, headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == movie_title

    # asserting for unauthorized user
    rating_data = {"rating": 4.0}
    rating_data2 = {"rating": 6.0}
    response = client.post(
        f"/ratings?movie_title={movie_title}",
        json=rating_data
    )

    assert response.status_code == 401

    # assertion for error(if not movie title)
    response = client.get(
        f"/ratings?movie_title", headers=auth_headers
    )
    assert response.status_code == 400

    # assertion for error(if already rating exceeds 5.0)
    response = client.post(
        f"/ratings?movie_title={movie_title}",
        json=rating_data2, headers=auth_headers
    )
    assert response.status_code == 400

    # add rating to movie
    response = client.post(
        f"/ratings?movie_title={movie_title}",
        json=rating_data, headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["movie"]["title"] == "rate_movie"
    assert data["rating"] == 4.0

    # assertion for error(if already rated)
    response = client.post(
        f"/ratings?movie_title={movie_title}",
        json=rating_data, headers=auth_headers
    )
    assert response.status_code == 400


def test_get_movie_rating(client, setup_database, auth_headers):

    # assertion for error(if not movie title)
    response = client.get(
        f"/ratings?movie_title", headers=auth_headers
    )
    assert response.status_code == 400

    # test to get ratings for a movie
    movie_title = "rate_movie"
    response = client.get(
        f"/ratings?movie_title={movie_title}", headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    response_data = data[0]
    assert response_data["id"] == 1
    assert response_data["rating"] == 4.0

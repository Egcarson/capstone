def test_add_comment(client, setup_database, auth_headers):

    # add a movie with the title for testing
    movie_title = "testing movie title"
    movie_data = {"title": movie_title, "genre": "Drama"}
    response = client.post(
        "/movies",
        json=movie_data, headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == movie_title

    comment_data = {"comment_text": "testing comment"}

    # asserting for unauthorized user
    response = client.post(
        f"/comments/?movie_title={movie_title}",
        json=comment_data
    )

    assert response.status_code == 401

    # test for adding comment to movie
    response = client.post(
        f"/comments/?movie_title={movie_title}",
        json=comment_data, headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "successfully added"
    assert data["data"]["comment_text"] == "testing comment"


def test_get_comments(client, setup_database, auth_headers):

    movie_title = "testing movie title"
    not_found = "wrong movie"

    # asserting error (404 - movie not found)
    response = client.get(
        f"/comments/{not_found}", headers=auth_headers)
    assert response.status_code == 404

    # get comments
    response = client.get(
        f"/comments/{movie_title}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    # print(data)
    response_data = data[0]
    assert response_data["user"]["username"] == "testuser1"
    assert response_data["id"] == 1


def test_reply(client, setup_database, auth_headers):

    # add reply to comment============================================================
    reply_data = {"comment_text": "testing comment reply"}

    # asserting error (404 - parent comment not found)
    response = client.post(
        "/comments/5/reply",
        json=reply_data, headers=auth_headers
    )

    assert response.status_code == 404

    # asserting error (401 - unauthorized)
    response = client.post(
        "/comments/1/reply",
        json=reply_data
    )

    assert response.status_code == 401

    response = client.post(
        "/comments/1/reply",
        json=reply_data, headers=auth_headers
    )

    assert response.status_code == 201
    data = response.json()
    assert data["parent_id"] == 1
    assert data["comment_text"] == "testing comment reply"

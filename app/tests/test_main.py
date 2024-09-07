def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "get-a-grip-api - create an account or login to access the API"
    }


def test_create_new_user(client):
    response = client.post(
        "/user/create",
        json={
            "username": "test_user",
            "email": "test@mail.com",
            "password": "test_password",
        },
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["username"] == "test_user"
    assert response_json["email"] == "test@mail.com"
    assert response_json["id"] == 12  # 11 seeded users already

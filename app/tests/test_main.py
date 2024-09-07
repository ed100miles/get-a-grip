def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "get-a-grip-api - create an account or login to access the API"
    }

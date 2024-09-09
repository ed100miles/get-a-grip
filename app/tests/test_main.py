from datetime import datetime

from ..constants import datetime_format
from ..seed_db import NUM_SEED_PINCHES_PER_USER, seed_users


def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "get-a-grip-api - create an account or login to access the API"
    }


class TestUserRoute:
    def test_create_new_user(self, client):
        response = client.post(
            "/user/create",
            json={
                "username": "test_user",
                "email": "test@testmail.com",
                "password": "test_password",
            },
        )
        assert response.status_code == 200
        assert (
            response.json()["message"]
            == "User created successfully - validate email to login"
        )
        assert isinstance(response.json()["minutes_to_validate"], int)

    def test_create_new_user_existing_email(self, client):
        response = client.post(
            "/user/create",
            json={
                "username": "test_user",
                "email": "test@mail.com",
                "password": "test_password",
            },
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Email already registered"

    def test_login(self, client):
        response = client.post(
            "/user/token",
            data={"username": "test", "password": "test"},  # test user seeded in db
        )
        assert response.status_code == 200
        response_json = response.json()
        assert isinstance(response_json["access_token"], str)
        assert response_json["token_type"] == "bearer"


class TestGraphQLRoute:
    def test_query_pinches(self, client, test_user_token):
        response = client.post(
            "/graphql",
            json={
                "query": """
                    query { 
                        pinches { 
                            id userId wide deep weight duration createdAt
                        }
                    }
                    """
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        assert response.status_code == 200
        response_json = dict(response.json())
        pinch_results = response_json["data"]["pinches"]
        assert len(pinch_results) == NUM_SEED_PINCHES_PER_USER * len(seed_users)
        assert pinch_results[0]["id"] == 1
        assert pinch_results[0]["userId"] == 1
        assert pinch_results[0]["duration"] == 6.5348866156918275
        assert pinch_results[0]["weight"] == 5.048719016670407
        assert pinch_results[0]["wide"]
        assert pinch_results[0]["deep"]
        # convert datetime string to datetime object to check it's valid
        datetime.strptime(pinch_results[0]["createdAt"], datetime_format)

    def test_mutation_add_pinch(self, client, test_user_token):
        response = client.post(
            "/graphql",
            json={
                "query": """
                    mutation {
                        addPinch(
                            wide: true,
                            deep: true,
                            weight: 5.0,
                            duration: 5.0
                        ) {
                            id userId wide deep weight duration createdAt
                        }
                    }
                    """
            },
            headers={"Authorization": f"Bearer {test_user_token}"},
        )
        assert response.status_code == 200
        response_json = dict(response.json())
        pinch_result = response_json["data"]["addPinch"]
        assert pinch_result["userId"] == 11
        assert pinch_result["wide"]
        assert pinch_result["deep"]
        assert pinch_result["weight"] == 5.0
        assert pinch_result["duration"] == 5.0
        # convert datetime string to datetime object to check it's valid
        datetime.strptime(pinch_result["createdAt"], datetime_format)
        assert pinch_result["id"] == NUM_SEED_PINCHES_PER_USER * len(seed_users) + 1

from datetime import datetime
from typing import Final

from ..seed_db import NUM_SEED_PINCHES_PER_USER, seed_users

datetime_format: Final = "%Y-%m-%dT%H:%M:%S.%f"


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
                "email": "test@mail.com",
                "password": "test_password",
            },
        )
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["username"] == "test_user"
        assert response_json["email"] == "test@mail.com"
        assert response_json["id"] == 12  # 11 seeded users already

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

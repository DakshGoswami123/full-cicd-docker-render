from app.main import create_app


def test_home_endpoint_returns_200():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"App Running" in response.data


def test_health_endpoint_returns_200():
    app = create_app()
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_info_endpoint_returns_metadata():
    app = create_app()
    client = app.test_client()

    response = client.get("/api/info")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["status"] == "running"
    assert "version" in payload

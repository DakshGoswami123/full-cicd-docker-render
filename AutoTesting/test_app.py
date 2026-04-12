import io

from app.main import create_app


def test_home_endpoint_returns_200():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"AI Resume Analyzer" in response.data


def test_health_endpoint_returns_200():
    app = create_app()
    client = app.test_client()

    response = client.get("/health?raw=1")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_info_endpoint_returns_metadata():
    app = create_app()
    client = app.test_client()

    response = client.get("/api/info?raw=1")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["status"] == "running"
    assert "version" in payload


def test_upload_endpoint_accepts_text_file():
    app = create_app()
    client = app.test_client()

    response = client.post(
        "/upload?raw=1",
        data={
            "resume_file": (io.BytesIO(b"Python Flask Docker SQL GitHub Actions"), "resume.txt"),
        },
        content_type="multipart/form-data",
    )

    payload = response.get_json()

    assert response.status_code == 200
    assert payload["word_count"] >= 5
    assert "Python" in payload["skills_found"]

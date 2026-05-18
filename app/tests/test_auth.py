# app/tests/test_auth.py
# Basic test for the auth page.

from app import create_app


def test_login_page():
    app = create_app()
    client = app.test_client()
    response = client.get('/auth/login')
    assert response.status_code == 200

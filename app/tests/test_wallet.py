# app/tests/test_wallet.py
# Basic test for the wallet page.

from app import create_app


def test_wallet_page():
    app = create_app()
    client = app.test_client()
    response = client.get('/wallet/')
    assert response.status_code == 200

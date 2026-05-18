# app/tests/test_payment.py
# Basic test for the payment page.

from app import create_app


def test_payment_page():
    app = create_app()
    client = app.test_client()
    response = client.get('/payment/make')
    assert response.status_code == 200

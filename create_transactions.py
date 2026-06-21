import requests

BASE = 'http://127.0.0.1:5000'

# Login as Ram
s = requests.Session()
s.post(f'{BASE}/login', data={'email': 'ram@epaisa.com', 'password': 'password123'})

# Load funds
s.post(f'{BASE}/api/load-funds', data={'amount': '10000', 'purpose': 'Demo load'})

# Send to Sita
s.post(f'{BASE}/api/send-money', data={'amount': '2500', 'phone': '9802222222', 'purpose': 'Payment'})

# Login as Sita
s = requests.Session()
s.post(f'{BASE}/login', data={'email': 'sita@epaisa.com', 'password': 'password123'})
s.post(f'{BASE}/api/load-funds', data={'amount': '5000', 'purpose': 'Demo load'})
s.post(f'{BASE}/api/send-money', data={'amount': '1000', 'phone': '9803333333', 'purpose': 'Transfer'})

print("Transactions created!")
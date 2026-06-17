"""
E-Paisa Demo Data Generator
Run this while your server is running to create test users
"""
import requests

BASE = 'http://127.0.0.1:5000'

# Test users to create
users = [
    ('Ram Sharma', 'ram@epaisa.com', '9801111111', 'password123'),
    ('Sita Devi', 'sita@epaisa.com', '9802222222', 'password123'),
    ('Hari Prasad', 'hari@epaisa.com', '9803333333', 'password123'),
    ('Gita Kumari', 'gita@epaisa.com', '9804444444', 'password123'),
]

print("Creating demo users...")
for name, email, phone, pwd in users:
    try:
        r = requests.post(f'{BASE}/register', data={
            'fullname': name,
            'email': email,
            'phone': phone,
            'password': pwd
        }, allow_redirects=True, timeout=5)
        if r.status_code == 200:
            print(f"  Created: {name} ({email})")
        else:
            print(f"  Failed: {name} - Status {r.status_code}")
    except Exception as e:
        print(f"  Error: {name} - {str(e)[:50]}")

print("\n" + "="*60)
print("Demo users created!")
print("="*60)
print("\nLogin credentials:")
print("  ram@epaisa.com    / password123")
print("  sita@epaisa.com   / password123")
print("  hari@epaisa.com   / password123")
print("  gita@epaisa.com   / password123")
print("\nAdmin:")
print("  admin@epaisa.com  / admin123")
print("="*60)

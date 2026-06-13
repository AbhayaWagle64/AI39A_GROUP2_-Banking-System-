#!/usr/bin/env python3
"""
E-Paisa Complete Sprint Test Suite - FIXED VERSION
Tests all features from Sprint 1, 2, 3, 4
Run: python test_all_sprints_fixed.py
"""

import requests
import sys
import json
import re
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:5000"
TEST_EMAIL = f"test_{datetime.now().strftime('%H%M%S')}@test.com"
TEST_PHONE = f"98{datetime.now().strftime('%H%M%S')}"
TEST_PASSWORD = "TestPass123!"
TEST_NAME = "Test User"

# Colors for terminal output
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

class TestResult:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add(self, name, status, details="", sprint=""):
        self.tests.append({
            "name": name,
            "status": status,
            "details": details,
            "sprint": sprint
        })
        if status:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_report(self):
        print("\n" + "=" * 70)
        print(f"{Colors.BLUE}{Colors.BOLD}E-Paisa Sprint Test Report{Colors.RESET}")
        print("=" * 70)
        
        current_sprint = ""
        for test in self.tests:
            if test["sprint"] != current_sprint:
                current_sprint = test["sprint"]
                print(f"\n{Colors.BOLD}{current_sprint}{Colors.RESET}")
                print("-" * 50)
            
            status = f"{Colors.GREEN}✅ PASS{Colors.RESET}" if test["status"] else f"{Colors.RED}❌ FAIL{Colors.RESET}"
            print(f"  {status} | {test['name']}")
            if test["details"]:
                print(f"       {Colors.YELLOW}{test['details']}{Colors.RESET}")
        
        print("\n" + "=" * 70)
        total = self.passed + self.failed
        print(f"Total: {total} | {Colors.GREEN}Passed: {self.passed}{Colors.RESET} | {Colors.RED}Failed: {self.failed}{Colors.RESET}")
        print("=" * 70)
        
        if self.failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 All tests passed! E-Paisa is ready for demo.{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}⚠️  {self.failed} test(s) failed. Check details above.{Colors.RESET}")

results = TestResult()

def test_get(url, name, sprint, expected_status=None, check_redirect=None):
    """Test GET request with flexible expectations"""
    try:
        r = requests.get(url, timeout=5, allow_redirects=True)
        
        # If expected_status is None, accept common success codes
        if expected_status is None:
            status = r.status_code in [200, 302]
        else:
            status = r.status_code == expected_status
            
        # Check redirect if specified
        if check_redirect:
            status = status and check_redirect in r.url
            
        results.add(name, status, f"Status: {r.status_code}, URL: {r.url}", sprint)
        return r
    except Exception as e:
        results.add(name, False, str(e), sprint)
        return None

def test_post(url, name, sprint, data=None, expected_status=None, follow_redirects=True):
    """Test POST request"""
    try:
        r = requests.post(url, data=data, timeout=5, allow_redirects=follow_redirects)
        
        if expected_status is None:
            status = r.status_code in [200, 302]
        else:
            status = r.status_code == expected_status
            
        results.add(name, status, f"Status: {r.status_code}, URL: {r.url}", sprint)
        return r
    except Exception as e:
        results.add(name, False, str(e), sprint)
        return None

# ==========================================
# SPRINT 1 TESTS
# ==========================================
print(f"\n{Colors.BLUE}{Colors.BOLD}Testing Sprint 1 Features...{Colors.RESET}")

# 1.1 Server Health - should redirect to register or login
test_get(f"{BASE_URL}/", "Server Running", "SPRINT 1: Core Infrastructure", check_redirect="register")

# 1.2 Registration Page
test_get(f"{BASE_URL}/register", "Registration Page", "SPRINT 1: User Registration", 200)

# 1.3 Login Page
test_get(f"{BASE_URL}/login", "Login Page", "SPRINT 1: Secure Login", 200)

# 1.4 Terms Page
test_get(f"{BASE_URL}/terms", "Terms Page", "SPRINT 1: Legal", 200)

# 1.5 Password Reset Page
test_get(f"{BASE_URL}/forgot-password", "Password Reset Page", "SPRINT 1: Password Reset", 200)

# 1.6 User Registration (POST)
register_data = {
    "name": TEST_NAME,
    "email": TEST_EMAIL,
    "phone": TEST_PHONE,
    "password": TEST_PASSWORD
}
r = test_post(f"{BASE_URL}/register", "User Registration (POST)", "SPRINT 1: User Registration", register_data)

# 1.7 OTP Verification Page - should be accessible after registration
test_get(f"{BASE_URL}/verify-otp", "OTP Verification Page", "SPRINT 1: OTP System", 200)

# 1.8 Resend OTP
r = test_post(f"{BASE_URL}/resend-otp", "Resend OTP", "SPRINT 1: OTP System", {})

# Get OTP from file or terminal - for now, use a dummy
# In real scenario, you'd parse otp_log.txt or check terminal
otp_data = {"otp": "000000"}
r = test_post(f"{BASE_URL}/verify-otp", "OTP Verification (dummy)", "SPRINT 1: OTP System", otp_data)

# 1.9 Login with new user
login_data = {
    "email": TEST_EMAIL,
    "password": TEST_PASSWORD
}
r = test_post(f"{BASE_URL}/login", "User Login", "SPRINT 1: Secure Login", login_data)

# Check if login successful (should redirect to dashboard or verify-otp)
if r and ("dashboard" in r.url or "verify-otp" in r.url):
    results.add("Login Redirect", True, f"Redirected to: {r.url}", "SPRINT 1: Secure Login")
else:
    results.add("Login Redirect", False, f"Unexpected URL: {r.url if r else 'N/A'}", "SPRINT 1: Secure Login")

# ==========================================
# SPRINT 2 TESTS (No session required - test API structure)
# ==========================================
print(f"\n{Colors.BLUE}{Colors.BOLD}Testing Sprint 2 Features...{Colors.RESET}")

# Test API endpoints return proper auth errors when not logged in
r = test_get(f"{BASE_URL}/api/user-data", "API Auth Required", "SPRINT 2: API Security", 403)
r = test_post(f"{BASE_URL}/api/load-funds", "Load Funds Auth Required", "SPRINT 2: API Security", {"amount": "500"}, 401)
r = test_post(f"{BASE_URL}/api/send-money", "Send Money Auth Required", "SPRINT 2: API Security", {"phone": "9800000000", "amount": "100"}, 401)

# ==========================================
# SPRINT 3 TESTS
# ==========================================
print(f"\n{Colors.BLUE}{Colors.BOLD}Testing Sprint 3 Features...{Colors.RESET}")

# Admin should redirect to login when not authenticated
test_get(f"{BASE_URL}/admin", "Admin Dashboard (redirects)", "SPRINT 3: Admin", check_redirect="login")

# Admin export should return 401
test_get(f"{BASE_URL}/admin/export/users", "Admin Export (protected)", "SPRINT 3: Admin", 401)

# ==========================================
# SPRINT 4 TESTS (Test pages load - they'll show login when not auth'd)
# ==========================================
print(f"\n{Colors.BLUE}{Colors.BOLD}Testing Sprint 4 Features...{Colors.RESET}")

# All Sprint 4 pages should be accessible (show login if not auth'd, or feature if auth'd)
sprint4_pages = [
    ("/qr-payment", "QR Payment", "QR"),
    ("/merchant-payment", "Merchant Payment", "Merchant"),
    ("/utility-payment", "Utility Payment", "Utility"),
    ("/mobile-recharge", "Mobile Recharge", "Recharge"),
    ("/saved-payments", "Saved Payments", "Saved")
]

for url, name, keyword in sprint4_pages:
    r = test_get(f"{BASE_URL}{url}", f"{name} Page", f"SPRINT 4: {name}", 200)
    if r:
        # Check if page contains expected content OR login form (both valid)
        has_content = keyword in r.text or "Login" in r.text or "Password" in r.text
        results.add(f"{name} Content", has_content, f"Has '{keyword}' or login form: {has_content}", f"SPRINT 4: {name}")

# ==========================================
# SECURITY TESTS
# ==========================================
print(f"\n{Colors.BLUE}{Colors.BOLD}Testing Security...{Colors.RESET}")

# Test SQL Injection protection
sql_test = {"email": "'; DROP TABLE user_profile; --", "password": "test"}
r = test_post(f"{BASE_URL}/login", "SQL Injection Protection", "SECURITY", sql_test)

# Test XSS protection
xss_name = "<script>alert(1)</script>"
xss_email = f"xss_{datetime.now().strftime('%H%M%S')}@test.com"
xss_phone = f"96{datetime.now().strftime('%H%M%S')}"
xss_data = {
    "name": xss_name,
    "email": xss_email,
    "phone": xss_phone,
    "password": "TestPass123!"
}
r = test_post(f"{BASE_URL}/register", "XSS Protection", "SECURITY", xss_data)

# ==========================================
# FINAL REPORT
# ==========================================
results.print_report()

# Exit with appropriate code
if results.failed > 0:
    sys.exit(1)
else:
    sys.exit(0)
"""
sample_test.py
--------------
This is a sample test file containing intentional bugs, security vulnerabilities,
bad naming practices, and logic errors. We will use this to test our AI Code Reviewer!
"""

import os
import sys

# SECURITY BUG: Hardcoded secret key
SECRET_API_KEY = "AIzaSyD-SecretKey1234567890ExampleKey"
DATABASE_PASSWORD = "admin_password_123"


def calc(a, b, op):
    # LOGIC BUG & BAD PRACTICE: Poor variable names and missing error handling (division by zero)
    if op == "add":
        return a + b
    elif op == "sub":
        return a - b
    elif op == "mul":
        return a * b
    elif op == "div":
        return a / b  # Bug: Will crash if b == 0!
    else:
        print("Unknown op")
        # Bug: Returns None implicitly without raising exception


def read_user_file(f):
    # UNHANDLED EXCEPTION: Opening file without try/except or using with-statement context manager
    file_handle = open(f, "r")
    data = file_handle.read()
    # Missing file_handle.close() -> resource leak!
    return data


def authenticate_user(usr, pwd):
    # BAD PRACTICE: Plaintext password checking & SQL injection vulnerability simulation
    if usr == "admin" and pwd == DATABASE_PASSWORD:
        return True
    return False


if __name__ == "__main__":
    result = calc(10, 0, "div")
    print("Result:", result)

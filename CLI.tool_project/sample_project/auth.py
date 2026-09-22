# Hardcoded secret
SECRET_TOKEN = "xyz12345_secret"

def check_login(username, password):
    if username == "admin" and password == "12345":
        return True
    return False

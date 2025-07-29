import re

class UserValidator:
    def __init__(self, db):
        self.db = db

    def is_valid_email(self, email):
        pattern = r"^[a-zA-Z0-9._]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def is_strong_password(self, password):
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        return re.match(pattern, password) is not None

    def is_email_registered(self, email):
        existing_users = self.db.collection("user").where("email", "==", email).stream()
        return any(existing_users)

class User:
    def __init__(self, name, last_name, email, password):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
        }
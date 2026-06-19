from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, db, username=None, password=None, full_name=None, 
                 email=None, phone=None, address=None, account_type='Savings', date_joined=None):
        super().__init__(db)
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.address = address
        self.account_type = account_type
        self.date_joined = date_joined

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'account_type': self.account_type,
            'date_joined': self.date_joined
        }
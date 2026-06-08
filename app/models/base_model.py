class BaseModel:
    def __init__(self, db):
        self.db = db

    def save(self):
        pass

    def delete(self):
        pass

    def find(self, id):
        pass

    def all(self):
        pass
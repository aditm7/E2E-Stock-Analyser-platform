import os

class Config:
    def __init__(self):
        self.ENV = "development"
        self.DEBUG = True
        self.PORT = os.environ.get("PORT")
        self.HOST = '127.0.0.1'
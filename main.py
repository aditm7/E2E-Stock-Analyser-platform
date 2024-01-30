from app import app
from app import Config

if __name__ == "__main__":
    app.run(host= Config.HOST,
            port= Config.PORT,
            debug= Config.DEBUG
            )
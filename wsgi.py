from flask import Flask
from flask_cors import CORS

from config import Config
from lib.sql import db
from App import api

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

CORS(app, supports_credentials=True)

app.register_blueprint(blueprint=api, url_prefix='/api')

if __name__ == "__main__":
    app.run()

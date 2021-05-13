from flask import Flask
from flask_cors import CORS

from settings import Config
from sql.model import db
from routes.api import api

app = Flask(__name__)
app.config.from_object(Config)

with app.app_context():
    db.init_app(app)
    db.create_all()

CORS(app, supports_credentials=True)

app.register_blueprint(blueprint=api, url_prefix='/api')

if __name__ == "__main__":
    app.run()

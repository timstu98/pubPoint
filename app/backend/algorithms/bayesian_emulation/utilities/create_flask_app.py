import os
import sys

from dotenv import load_dotenv

from flask import Flask
from models import db

def load_environment():
    if "/app" not in sys.path:
        print("Ensure you set the PYTHONPATH to ensure relative imports work correctly.")

    load_dotenv(dotenv_path="/app/.env")
    return {
        "DB_USER": os.getenv("MYSQL_USER", "user"),
        "DB_PASSWORD": os.getenv("MYSQL_PASSWORD", "password"),
        "DB_HOST": os.getenv("MYSQL_HOST", "mysql"),
        "DB_NAME": os.getenv("MYSQL_DATABASE", "DB_NAME"),
        "API_KEY": os.getenv("API_KEY", "api_key"),
        "DATABASE_URI": f"mysql+pymysql://{os.getenv('MYSQL_USER', 'user')}:{os.getenv('MYSQL_PASSWORD', 'password')}@{os.getenv('MYSQL_HOST', 'mysql')}/{os.getenv('MYSQL_DATABASE', 'DB_NAME')}",
        "TEST_FUNCTIONALITY_MODE": os.getenv("TEST_FUNCTIONALITY_MODE", "false").lower() == "true"
    }

def create_flask_app():
    env = load_environment()
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = env["DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app, env
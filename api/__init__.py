from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config  # Проверьте, что ваш файл конфигурации импортируется корректно

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)  # Убедитесь, что SQLAlchemy инициализирован с `init_app`

    with app.app_context():
        db.create_all()  # Создаёт таблицы, если их нет

    return app

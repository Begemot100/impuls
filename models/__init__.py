from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()  # Экземпляр SQLAlchemy для использования в моделях
migrate = Migrate()  # Экземпляр Flask-Migrate для миграций

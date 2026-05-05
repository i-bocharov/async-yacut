import os
from flask import Flask
from dotenv import load_dotenv

from .extensions import db, migrate, csrf
from .config import config_map
from .api_views import api_bp
from .views import web_bp
from .error_handlers import register_error_handlers
from . import models  # noqa: F401 (регистрация метаданных для SQLAlchemy)

load_dotenv()


def create_app(config_name: str | None = None) -> Flask:
    """
    Application Factory: создаёт и настраивает экземпляр Flask-приложения.

    :param config_name: Имя конфигурации из config_map.
        По умолчанию берётся из env.
    :return: Настроенное приложение Flask.
    """
    env: str = os.getenv('FLASK_ENV', 'default')
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(
        config_map.get(config_name or env, config_map['default'])
    )
    os.makedirs(app.instance_path, exist_ok=True)

    # Инициализация расширений
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Прямая регистрация Blueprint'ов и обработчиков. Без обёрток register().
    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)
    register_error_handlers(app)

    return app


# Глобальный экземпляр для 'flask run', 'flask shell' и импортов в тестах
app: Flask = create_app()
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from typing import Final

# Экземпляры расширений создаются один раз и не перезаписываются
db: Final[SQLAlchemy] = SQLAlchemy()
migrate: Final[Migrate] = Migrate()
csrf: Final[CSRFProtect] = CSRFProtect()


def init_extensions(app: Flask) -> None:
    """Привязывает расширения к текущему экземпляру приложения."""
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
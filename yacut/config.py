import os
from typing import Final


class Config:
    """Базовая конфигурация Flask-приложения."""
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-prod')
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        'DATABASE_URI', 'sqlite:///instance/yacut.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    WTF_CSRF_ENABLED: bool = True
    DISK_TOKEN: str = os.getenv('DISK_TOKEN', '')
    YADISK_API_BASE_URL: str = os.getenv(
        'YADISK_API_BASE_URL',
        'https://cloud-api.yandex.net/v1/disk/resources'
    )
    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024  # 16 MB limit


class DevelopmentConfig(Config):
    """Настройки для локальной разработки."""
    DEBUG: bool = True


class TestingConfig(Config):
    """Настройки для автоматических тестов."""
    TESTING: bool = True
    WTF_CSRF_ENABLED: bool = False


class ProductionConfig(Config):
    """Настройки для боевого окружения."""
    DEBUG: bool = False
    WTF_CSRF_SSL_STRICT: bool = True


# Карта конфигураций не меняется в рантайме
config_map: Final[dict[str, type[Config]]] = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
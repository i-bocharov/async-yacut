from flask import Flask, Response, jsonify, render_template, request
from .extensions import db


def register_error_handlers(app: Flask) -> None:
    """Регистрирует глобальные обработчики ошибок 404 и 500."""

    @app.errorhandler(404)
    def not_found(error: Exception) -> tuple[Response | str, int]:
        """Возвращает JSON-ответ для API или HTML-шаблон для браузера."""
        if request.path.startswith('/api/'):
            return jsonify(message='Указанный id не найден'), 404
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(error: Exception) -> tuple[Response | str, int]:
        """Откатывает транзакцию БД и возвращает ответ об ошибке сервера."""
        db.session.rollback()
        if request.path.startswith('/api/'):
            return jsonify(message='Внутренняя ошибка сервера'), 500
        return render_template('errors/500.html'), 500
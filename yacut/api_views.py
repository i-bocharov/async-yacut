from __future__ import annotations
from typing import Final
from flask import Blueprint, Response, jsonify, request
from sqlalchemy import select

from yacut.extensions import db
from yacut.models import URLMap
from yacut.services.shortener import get_unique_short_id

api_bp: Final[Blueprint] = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/id/', methods=['POST'])
def create_short_link() -> tuple[Response, int]:
    """Создаёт короткую ссылку через REST API."""
    # Проверка наличия JSON-тела
    if not request.is_json or request.get_json(silent=True) is None:
        return jsonify(message='Отсутствует тело запроса'), 400

    data: dict[str, str] = request.get_json()

    # Валидация обязательного поля
    if 'url' not in data or not data['url']:
        return jsonify(message='"url" является обязательным полем!'), 400

    original_url: str = data['url']
    custom_id: str | None = data.get('custom_id')

    # Пустая строка трактуется как отсутствие пользовательского ID
    if custom_id == '':
        custom_id = None

    # Генерация или проверка уникальности
    try:
        short_id: str = get_unique_short_id(custom_id)
    except ValueError as exc:
        return jsonify(message=str(exc)), 400
    except RuntimeError:
        return jsonify(
            message='Не удалось сгенерировать уникальный идентификатор'
        ), 500

    # Сохранение в БД
    new_link: URLMap = URLMap(original=original_url, short=short_id)
    db.session.add(new_link)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify(
            message='Предложенный вариант короткой ссылки уже существует.'
        ), 400

    # Формирование ответа
    base_url: str = request.host_url.rstrip('/')
    short_url: str = f'{base_url}/{new_link.short}'

    return jsonify(url=original_url, short_link=short_url), 201


@api_bp.route('/id/<short_id>/', methods=['GET'])
def get_original_link(short_id: str) -> tuple[Response, int]:
    """Возвращает оригинальную ссылку по короткому идентификатору."""
    url_map: URLMap | None = db.session.scalar(
        select(URLMap).filter_by(short=short_id)
    )
    if not url_map:
        return jsonify(message='Указанный id не найден'), 404

    return jsonify(url=url_map.original), 200
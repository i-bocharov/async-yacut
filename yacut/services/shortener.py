import random
import re
import string
from typing import Final
from sqlalchemy import select

from yacut.extensions import db
from yacut.models import URLMap

SHORT_ID_LENGTH: Final[int] = 6
ALPHABET: Final[str] = string.ascii_letters + string.digits
RESERVED_WORDS: Final[set[str]] = {'files'}
CUSTOM_ID_PATTERN: Final[re.Pattern] = re.compile(r'^[a-zA-Z0-9]{1,16}$')


def get_unique_short_id(custom_id: str | None = None) -> str:
    """
    Валидирует пользовательский short_id или генерирует уникальный
    автоматически.

    :param custom_id: Пользовательский вариант короткой ссылки.
    :return: Валидный и уникальный short_id.
    :raises ValueError: Если ID не соответствует формату или уже занят.
    :raises RuntimeError: Если не удалось сгенерировать уникальный ID
        за 10 попыток.
    """
    if custom_id:
        if not CUSTOM_ID_PATTERN.fullmatch(custom_id):
            raise ValueError(
                'Указано недопустимое имя для короткой ссылки'
            )

        if custom_id in RESERVED_WORDS or db.session.scalar(
            select(URLMap).filter_by(short=custom_id)
        ):
            raise ValueError(
                'Предложенный вариант короткой ссылки уже существует.'
            )
        return custom_id

    for _ in range(10):
        new_id = ''.join(random.choices(ALPHABET, k=SHORT_ID_LENGTH))
        if not db.session.scalar(select(URLMap).filter_by(short=new_id)):
            return new_id

    raise RuntimeError(
        'Не удалось сгенерировать уникальный идентификатор'
    )
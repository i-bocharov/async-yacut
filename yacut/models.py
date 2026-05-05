from datetime import datetime
from .extensions import db


class URLMap(db.Model):  # type: ignore[name-defined]
    """Модель соответствия оригинальной ссылки и короткого идентификатора."""
    __tablename__ = 'url_map'

    id: int = db.Column(db.Integer, primary_key=True)
    original: str = db.Column(db.String(256), nullable=False)
    short: str = db.Column(
        db.String(16), unique=True, nullable=False, index=True
    )
    timestamp: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self) -> dict[str, int | str | datetime]:
        """Сериализует объект модели в словарь для API-ответов."""
        return {
            'id': self.id,
            'original': self.original,
            'short': self.short,
            'timestamp': self.timestamp,
        }
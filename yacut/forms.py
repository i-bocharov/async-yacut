from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField
from wtforms.validators import DataRequired, URL, Optional, Regexp


class ShortenForm(FlaskForm):
    """Форма для главной страницы: сокращение ссылок."""
    original_link: StringField = StringField(
        'Оригинальная ссылка',
        validators=[
            DataRequired(message='Поле обязательно для заполнения'),
            URL(message='Введите корректный URL')
        ]
    )
    custom_id: StringField = StringField(
        'Пользовательский идентификатор',
        validators=[
            Optional(),
            Regexp(
                r'^[a-zA-Z0-9]{1,16}$',
                message='Указано недопустимое имя для короткой ссылки'
            )
        ]
    )


class UploadForm(FlaskForm):
    """Форма для страницы загрузки файлов."""
    files: FileField = FileField(
        'Выберите файлы',
        validators=[FileRequired(message='Выберите хотя бы один файл')],
        render_kw={'multiple': True}  # Позволяет выбор нескольких файлов
    )
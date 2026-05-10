from __future__ import annotations
import asyncio
from typing import Final, cast
from flask import Blueprint, Response, current_app, render_template, request
from flask import abort
from werkzeug.datastructures import FileStorage
from werkzeug.utils import redirect as werkzeug_redirect
import aiohttp
from urllib.parse import quote, unquote

from yacut.extensions import db
from yacut.forms import ShortenForm, UploadForm
from yacut.models import URLMap
from yacut.services.shortener import get_unique_short_id
from yacut.services.yadisk import (
    REQUEST_UPLOAD_URL,
    DOWNLOAD_LINK_URL,
    APP_FOLDER_PREFIX,
    LOCATION_DISK_PREFIX,
)

web_bp: Final[Blueprint] = Blueprint('web', __name__)


async def _upload_file_to_disk(
    file: FileStorage, token: str
) -> str:
    """Загружает файл на Яндекс Диск и возвращает прямую ссылку."""
    headers: dict[str, str] = {'Authorization': f'OAuth {token}'}
    filename: str = file.filename or ''
    path: str = f'{APP_FOLDER_PREFIX}{quote(filename)}'

    async with aiohttp.ClientSession() as session:
        # Получение ссылки для загрузки
        async with session.get(
            REQUEST_UPLOAD_URL, headers=headers, params={'path': path}
        ) as resp:
            upload_data: dict = await resp.json()
            if 'href' not in upload_data:
                raise ValueError(
                    f'Yandex Disk API error: {upload_data}'
                )
            upload_href: str = upload_data['href']

        # Загрузка файла (без Authorization, как требует API)
        file_data: bytes = file.read()
        async with session.put(upload_href, data=file_data) as resp:
            resp.raise_for_status()
            # Обработка Location: декодируем и убираем /disk
            location: str = resp.headers.get('Location', '')
            file_path: str = unquote(location).replace(
                LOCATION_DISK_PREFIX, ''
            ).replace('app:', '', 1).lstrip('/')

        # Получение ссылки на скачивание
        async with session.get(
            DOWNLOAD_LINK_URL, headers=headers,
            params={'path': file_path}
        ) as resp:
            download_data: dict = await resp.json()
            if 'href' not in download_data:
                raise ValueError(
                    f'Yandex Disk API error: {download_data}'
                )
            return download_data['href']


@web_bp.route('/', methods=['GET', 'POST'])
def index() -> Response | str:
    """Главная страница: форма сокращения ссылок."""
    form: ShortenForm = ShortenForm()
    if form.validate_on_submit():
        try:
            short_id: str = get_unique_short_id(form.custom_id.data)
        except ValueError as exc:
            form.custom_id.errors.append(str(exc))
            return render_template('index.html', form=form)

        new_link: URLMap = URLMap(
            original=form.original_link.data,
            short=short_id,
        )
        db.session.add(new_link)
        db.session.commit()

        short_url: str = (
            f'{request.host_url.rstrip("/")}/{new_link.short}'
        )
        return render_template(
            'index.html', form=form, short_url=short_url
        )

    return render_template('index.html', form=form)


@web_bp.route('/<short_id>')
def redirect_to_url(short_id: str) -> Response:
    """Переадресация по короткой ссылке."""
    url_map: URLMap | None = db.session.scalar(
        db.select(URLMap).filter_by(short=short_id)
    )
    if not url_map:
        abort(404)
    return cast(
        Response, werkzeug_redirect(url_map.original, code=302)
    )


@web_bp.route('/files', methods=['GET', 'POST'])
def upload_files() -> Response | str:
    """Страница загрузки файлов на Яндекс Диск."""
    form: UploadForm = UploadForm()
    if form.validate_on_submit():
        files: list[FileStorage] = request.files.getlist('files')
        token: str = current_app.config['DISK_TOKEN']

        async def process_uploads() -> list[tuple[str, str, str]]:
            # Параллельная загрузка всех файлов на Яндекс Диск
            upload_coroutines = [
                _upload_file_to_disk(f, token) for f in files
            ]
            direct_links: list[str] = await asyncio.gather(*upload_coroutines)

            # Генерация идентификаторов и сбор данных
            return [
                (f.filename or '', link, get_unique_short_id())
                for f, link in zip(files, direct_links)
            ]

        uploaded_links: list[tuple[str, str, str]] = asyncio.run(
            process_uploads()
        )

        # Запись в БД одной транзакцией после успешной загрузки всех файлов
        results: list[dict[str, str]] = []
        host: str = request.host_url.rstrip('/')
        for fname, direct_link, short_id in uploaded_links:
            new_link: URLMap = URLMap(original=direct_link, short=short_id)
            db.session.add(new_link)
            results.append({
                'filename': fname,
                'short_url': f'{host}/{short_id}',
            })
        db.session.commit()

        return render_template(
            'files.html', form=form, uploaded_links=results
        )

    return render_template('files.html', form=form)
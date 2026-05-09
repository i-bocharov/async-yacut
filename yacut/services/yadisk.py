import os
from typing import Final

from dotenv import load_dotenv

load_dotenv()

# Базовые параметры
API_HOST: Final[str] = os.getenv(
    'YADISK_API_HOST', 'https://cloud-api.yandex.net/'
)
API_VERSION: Final[str] = os.getenv('YADISK_API_VERSION', 'v1')

# Эндпоинты (собираются из базовых параметров)
REQUEST_UPLOAD_URL: Final[str] = (
    f'{API_HOST}{API_VERSION}/disk/resources/upload'
)
DOWNLOAD_LINK_URL: Final[str] = (
    f'{API_HOST}{API_VERSION}/disk/resources/download'
)
DISK_INFO_URL: Final[str] = f'{API_HOST}{API_VERSION}/disk/'

# Служебные константы
APP_FOLDER_PREFIX: Final[str] = 'app:/'
LOCATION_DISK_PREFIX: Final[str] = '/disk'
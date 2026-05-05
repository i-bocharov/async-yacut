from flask import Blueprint
from typing import Final

web_bp: Final[Blueprint] = Blueprint('web', __name__)
"""Blueprint для веб-интерфейса (главная, /files, редиректы)."""
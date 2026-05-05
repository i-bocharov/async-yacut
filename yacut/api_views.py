from flask import Blueprint
from typing import Final

api_bp: Final[Blueprint] = Blueprint('api', __name__, url_prefix='/api')
"""Blueprint для REST API-эндпоинтов (/api/id/ и др.)."""
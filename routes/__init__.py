from flask import Blueprint

main_bp = Blueprint('main', __name__)
deck_bp = Blueprint('deck', __name__)
assets_bp = Blueprint('assets', __name__)

from .main_routes import *
from .deck_routes import *
from .asset_routes import *

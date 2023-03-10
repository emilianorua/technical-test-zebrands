from flask import jsonify
from flask import Blueprint

bp_main = Blueprint('main', __name__)


@bp_main.route('/')
def index():
    data = {'message': 'Technical test from Zebrands interview'}
    return jsonify(data)

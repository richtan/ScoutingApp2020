from flask import Flask, request, Blueprint
import flask

bp = Blueprint('index', __name__, template_folder='templates')


@bp.route('/', methods=['GET'])
def handle():
    return flask.render_template('index.html')

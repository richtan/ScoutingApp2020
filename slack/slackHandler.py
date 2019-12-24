from flask import Flask, request, Blueprint, render_template, current_app
import random
import time
bp = Blueprint('slack', __name__)



@bp.route('/match', methods=['POST'])
def slackmatch():
    return "hello"


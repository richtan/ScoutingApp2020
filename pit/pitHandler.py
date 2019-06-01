from flask import Flask, request, Blueprint, render_template, current_app
from .batteryTracker import batteryTracker
from .matchSchedule import matchSchedule
bp = Blueprint('pit', __name__)


@bp.route('/')
@bp.route('/home', methods=['GET', 'POST'])
def home():
    scraper = current_app._get_current_object().scraper
    battery1, battery2, battery3, battery4, battery5, battery6, battery7, battery8, battery9, battery10, battery11 = batteryTracker(
        current_app._get_current_object().database, request)
    AP1, OT1, T1, AP2, OT2, T2, URL, C1, C2 = matchSchedule(scraper)

    print(battery1, battery2, battery3)
    return render_template('pit.html', C1=C1, C2=C2, url=URL, one=battery1, two=battery2, three=battery3, four=battery4, five=battery5, six=battery6, seven=battery7, eight=battery8, nine=battery9, ten=battery10, eleven=battery11, AP1=AP1, OT1=OT1, T1=T1, AP2=AP2, OT2=OT2, T2=T2)

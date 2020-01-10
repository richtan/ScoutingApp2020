from flask import Flask, request, Blueprint, render_template, current_app, jsonify
import random
import time
import re
import json
bp = Blueprint('slack', __name__)



@bp.route('/match', methods=['POST'])
def slackmatch():
    sqllite = current_app._get_current_object().sqllite
    datascraper = current_app._get_current_object().scraper
    match_num = request.form.get('text', None).strip()
    if(re.search("^[0-9]*$", match_num) is None):
        return jsonify({'response_type': 'in_channel','text': 'Enter match number as a positive integer'})
    match = sqllite.get_match_info(match_num)
    teams = ['R1','R2','R3','B1','B2','B3']
    attachments = []
    for team in teams:
        stats = match.get(team)
        stat_section = lambda title, value: {
                    "title": "*%s*" % (title),
                    "value": value,
                    "short": True
                }
        fields = []
        for stat in stats:
            fields.append(stat_section(stat, str(stats[stat])))
        if str(stats["TEAMNUM"])!="972":
            attachments.append({
			"color": "#FF3333" if team[0]=="R" else "#3333FF",
            "author_name": str(stats["TEAMNUM"]),
            "author_link": "http://flickr.com/bobby/",
            "author_icon": "https://placeimg.com/16/16/people",
            "title": datascraper.getSecretTeamInfo(str(stats["TEAMNUM"]))["nickname"],
            "fields": fields,
            "callback_id": "more_" + str(stats["TEAMNUM"]),
            "actions": [{
                "name": "more_" + str(stats["TEAMNUM"]),
                "text": "More Info",
                "type": "button"
            }]
		})
    
    return jsonify({'response_type': 'in_channel','text': '*Match ' + match_num + ':*','attachments': attachments})

@bp.route('/team', methods=['POST'])
def slackteam():
    sqllite = current_app._get_current_object().sqllite
    team_num = request.form.get('text', None)
    team_info = sqllite.get_team_info(team_num)
    attachments = []

    
    return jsonify({'response_type': 'in_channel','text': '*Match ' + match_num + ':*','attachments': attachments}) 

@bp.route('/action', methods=['POST'])
def slackaction():
    payload = json.loads(request.payload)
    if payload.actions[0].name.startswith('more_'):
        return flask.redirect(flask.url_for('team'), code=307)
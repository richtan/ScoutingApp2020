from flask import Flask, request, Blueprint, render_template, current_app, jsonify
import random
import time
bp = Blueprint('slack', __name__)



@bp.route('/match', methods=['POST'])
def slackmatch():
    sqllite = current_app._get_current_object().sqllite
    match = sqllite.get_match_info(request.form.get('text', None))
    teams = ['R1','R2','R3','B1','B2','B3']
    blocks = []
    for team in teams:
        blocks.append({"type": "divider"})
        blocks.append({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": team + ' ' + str(match.get(team))
			},
            "accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "More Info",
					"emoji": True
				},
				"value": "click_me_123"
			},

		})


    return jsonify({
    'response_type': 'in_channel',
	"blocks":blocks
})



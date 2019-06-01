import flask
from flask import current_app, session, render_template, redirect
import time
import requests as rq


def matchScouting(request):
    database = current_app._get_current_object().database
    scraper = current_app._get_current_object().scraper
    if request.method == "GET":
        return flask.render_template('/matchScouting/inputMatchNumber.html')
    elif request.method == "POST":
        fields = [k for k in request.form]
        values = [request.form[k] for k in request.form]

        data = dict(zip(fields, values))
        print(data)
        if ('teamNumber' in fields):
            session['teamnumber'] = data['teamNumber']
            if False:  # implement later
                return flask.render_template('/matchScouting/inputMatchNumber.html')
            return flask.render_template('/AlanMatchScouting.html', matchNumber=request.form['matchNumber'], teamNumber=request.form['teamNumber'])

        if('matchNumber' in fields):

            if not data['matchNumber'] or not data['matchNumber'].isdigit():
                return redirect("/scouting/inputMatchData")

            # already people scouting teams, need to implement
            datateams = ["254", "1323"]
            teamlist = ['R1', 'R2', 'R3', 'B1', 'B2', 'B3']

            teams = scraper.getMatchTeams(data["matchNumber"])
            {teams.update(
                {k: "Taken: "+teams[k]}): 0 for k in teams if teams[k] in datateams}
            print(teams)
            session['matchid'] = data['matchNumber']
            return flask.render_template('/matchScouting/inputTeamNumber.html', matchNumber=request.form['matchNumber'],
                                         R1=teams['R1'],
                                         R2=teams['R2'],
                                         R3=teams['R3'],
                                         B1=teams['B1'],
                                         B2=teams['B2'],
                                         B3=teams['B3'],)

        # example data: {'climbTime': '10', 'cargo': '1,2,1,0,', 'matchNum': '12345', 'comments': 'Comments here', 'climbLevel': 'Level 1', 'teamNum': '12345', 'hatch': '1,1,1,2,', 'sandstorm': 'idk'}
        newdata = {"type": "match", "MatchID": '', 'Defense': '', 'Fouls': '', "TeamNumber": '', 'Climb': '', 'BuddyClimb': '', 'ClimbTime': '',
                   'TopH': '', 'MidH': '', 'LowH': '', 'CarH': '', 'CarC': '', 'LowC': '', 'MidC': '', 'TopC': '', 'Comments': '', 'Sandstorm': '', 'ScoutName': '', 'CrossedHabLine': 'Did not', 'SandstormCargo': '0', 'SandstormHatchesRocket': '0', 'SandstormHatchesCS': '0', "FailedHatch": "", "FailedCargo": "", "DriverLocation": ""}

        try:
            newdata.update({"MatchID": session['matchid'], 'Defense': data['defense'], 'Fouls': data['fouls'], "TeamNumber": session['teamnumber'], 'Climb': data['climb'], 'BuddyClimb': data['buddyClimbNum'], 'ClimbTime': data['climbTime'],
                            'TopH': data['h3'], 'MidH': data['h2'], 'LowH': data['h1'], 'CarH': data['hc'], 'CarC': data['cc'], 'LowC': data['c1'], 'MidC': data['c2'], 'TopC': data['c3'], 'Comments': data['comments'], 'Sandstorm': data['sandstorm'], 'ScoutName': data['name'], 'CrossedHabLine': data['sshab'], 'SandstormCargo': data['sscargo'], 'SandstormHatchesRocket': data['sshatchr'], 'SandstormHatchesCS': data['sshatchc'], "FailedHatch": data['fh'], "FailedCargo": data["fc"], "DriverLocation": session["indexnumber"]})
        except:
            return "Stop Hacking Us. "
        rq.post("https://script.google.com/macros/s/AKfycbzJb8ch1pg5vSCx8dAoTHEQwwn5SjfcGsWa7GpP4mb4-C20tq0G/exec?key=1XfIrmB9tNzBckh3W689WZToBLRnU2kwWatePk_pawoc", params=newdata, data=newdata)

        return render_template("fullScreenBill.html", url="https://belikebill.ga/billgen-API.php?default=1")

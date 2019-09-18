import flask
from flask import current_app, session, render_template, redirect
import time
import requests as rq
from .formFromJson import makeHTML


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
            taken = database.getVariable("takenRobots")
            

            if data['teamNumber'] in taken[session["matchid"]]:  # implement later
                return flask.render_template('/matchScouting/inputMatchNumber.html')
            taken[session["matchid"]].append(data["teamNumber"])
            #return flask.render_template('/AlanMatchScouting.html', matchNumber=request.form['matchNumber'], teamNumber=request.form['teamNumber'])
            return makeHTML().replace("{{matchNumber}}", request.form['matchNumber']).replace("{{teamNumber}}", request.form['teamNumber'])
        if('matchNumber' in fields):

            if not data['matchNumber'] or not data['matchNumber'].isdigit():
                return redirect("/scouting/inputMatchData")

            taken = database.getVariable("takenRobots")
            if not (data["matchNumber"] in taken):
                taken[data["matchNumber"]]=[]

            datateams = taken[data["matchNumber"]]
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
        try:
            data.update({"MatchID": session['matchid'], "TeamNumber": session['teamnumber'], "key":'1iXYDM1RxiohklB5mpEAWVOntMR9DzWMICej5GAz28FI', "type":"match"})
        except Exception as e:
            return e

        print(data)
        rq.post("https://script.google.com/macros/s/AKfycbxuJhaW4NcmsRJ80wDPoSevQON7347FTIyyL09qB-T5njpLgaZm/exec?key=1iXYDM1RxiohklB5mpEAWVOntMR9DzWMICej5GAz28FI", params=data, data=data)

        return render_template("fullScreenBill.html", url="https://belikebill.ga/billgen-API.php?default=1")

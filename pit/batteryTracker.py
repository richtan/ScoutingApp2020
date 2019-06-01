from flask import render_template
import time


def batteryTracker(database, request):
    if request.method == "GET":
        database.storeVariable('batteryStatus', ["good" if it < time.time(
        ) else "bad" for it in database.getVariable('timeUntilGood')])
        return database.getVariable('batteryStatus')[0], database.getVariable('batteryStatus')[1], database.getVariable('batteryStatus')[2], database.getVariable('batteryStatus')[3], database.getVariable('batteryStatus')[4], database.getVariable('batteryStatus')[5], database.getVariable('batteryStatus')[6], database.getVariable('batteryStatus')[7], database.getVariable('batteryStatus')[8], database.getVariable('batteryStatus')[9], database.getVariable('batteryStatus')[10]

    if request.method == "POST":
        print(request.form)
        if request.form["state"] in list('123456789')+['10', '11']:
            batteryStatus = database.getVariable("batteryStatus")
            batteryStatus[int(request.form["state"])-1] = "bad"
            database.storeVariable('batteryStatus', batteryStatus)
            timeUntilGood = database.getVariable('timeUntilGood')
            batteryChargingTime = database.getVariable("batteryChargingTime")

            timeUntilGood[int(request.form["state"])-1
                          ] = time.time()+batteryChargingTime
            database.storeVariable('batteryStatus', batteryStatus)

        return database.getVariable('batteryStatus')[0], database.getVariable('batteryStatus')[1], database.getVariable('batteryStatus')[2], database.getVariable('batteryStatus')[3], database.getVariable('batteryStatus')[4], database.getVariable('batteryStatus')[5], database.getVariable('batteryStatus')[6], database.getVariable('batteryStatus')[7], database.getVariable('batteryStatus')[8], database.getVariable('batteryStatus')[9], database.getVariable('batteryStatus')[10]

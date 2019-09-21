import flask
from flask import current_app, session, render_template, redirect
import time

import json 

def changeForm(request):
    if request.method=="GET":
        with open("scouting/formData.json", "r") as form:
            return render_template("changeForm.html", json=form.read())
    if request.method=="POST":
        with open("scouting/formData.json", "w") as form:
            form.write(str(request.form['json']))
            return redirect("/scouting/home")
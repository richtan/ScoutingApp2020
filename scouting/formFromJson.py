import flask
from flask import current_app, session, render_template, redirect
import time
import requests as rq

def makeShortTextInput(custom):
    return """<section class="inputSection"><h3>%s</h3> <div class="textInput"> <textarea type="text" name="%s" placeholder="%s" rows="1" maxlength="31">%s</textarea> </div></section>"""%(custom["Title"], custom["Name"], custom["Placeholder"], custom["DefaultName"])
def makeHeader(custom):
    return """<section class="headerSection"><h3>%s</h3></section>"""% (custom["Title"])
def makeOptions(custom):
    start = """<section class="inputSection"><h3>%s</h3><div class="optionInput">"""% (custom["Title"])
    name = custom["Name"]
    for option in custom["Options"]:
        ID = name+' '+option
        start+="""<input id="%s" type="radio" name="%s" value="%s" checked=""><label for="%s">%s</label>""" %(ID, name, option, ID, option)
    return start + """</div> </section>"""
def makeNumber(custom):
    return """<section class="inputSection"><h3>%s</h3>            <div class="numberInput">                <button type="button" class="sub">-</button>                <div class="numberFieldWrapper"><input type="number" name="%s" min="%s" max="%s" value="0"                        readonly=""></div>                <button type="button" class="add">+</button>            </div>        </section>"""%(custom['Title'], custom["Name"], custom["Min"], custom["Max"])
def makeTextInput(custom):
    return """<section class="inputSection"><h3>%s</h3><div class="textInput">   <textarea type="text" name="%s" placeholder="%s" rows="6"                   maxlength="255"></textarea>           </div>       </section>""" %(custom["Title"], custom["Name"], custom["Placeholder"])
def makeHTML():
    data=[{"Type": "ShortTextInput", "Title":"Scouter's Name","Placeholder": "Type here", "DefaultName": "", "Name": "Name"}, 
        {"Type":"Header", "Title": "Sandstorm"}, 
        {"Type":"Options", "Title": "Hab Level", "Options":["Level 1", "Level 2"], "Name": "HabLevel"}, 
        {"Type":"Options", "Title": "Hab Line", "Options":["Crossed", "Not Crossed"], "Name": "HabLine"}, 
        {"Type":"Number", "Title":"Cargo Ship", "Min": '0', "Max": '10', "Name": "SCS"}, 
        {"Type":"Number", "Title":"Rocket L1", "Min": '0', "Max": '10', "Name": "SL1"}, 
        {"Type":"Number", "Title":"Rocket L2", "Min": '0', "Max": '10', "Name": "SL2"},
        {"Type":"Number", "Title":"Rocket L3", "Min": '0', "Max": '10', "Name": "SL3"},
        {"Type":"Number", "Title":"Drop", "Min": '0', "Max": '10', "Name": "SL4"},
        {"Type":"Header", "Title": "Teleoperated Period"}, 
        {"Type":"Number", "Title":"Cargo Ship", "Min": '0', "Max": '10', "Name": "TCS"}, 
        {"Type":"Number", "Title":"Rocket L1", "Min": '0', "Max": '10', "Name": "TL1"}, 
        {"Type":"Number", "Title":"Rocket L2", "Min": '0', "Max": '10', "Name": "TL2"},
        {"Type":"Number", "Title":"Rocket L3", "Min": '0', "Max": '10', "Name": "TL3"},
        {"Type":"Number", "Title":"Drop", "Min": '0', "Max": '10', "Name": "TL4"},
        {"Type":"Header", "Title": "Endgame"},
        {"Type":"Number", "Title":"Climb Level", "Min": '0', "Max": '3', "Name": "ClimbLevel"},
         {"Type":"Options", "Title": "Buddy Climb", "Options":["Lifted Others", "Got Lifted"], "Name": "BuddyClimb"}, 
        {"Type":"Header", "Title":"Misc"},
        {"Type":"Options", "Title": "Played Defense", "Options":["Yes", "No"], "Name": "PlayedDefense"}, 
        {"Type":"Number", "Title":"Defense Ability (0 if N.A.)", "Min": '0', "Max": '5', "Name": "DefenseAbility"},

        {"Type":"Options", "Title": "Defended On", "Options":["Yes", "No"], "Name": "DefendedOn"}, 
        {"Type":"Options", "Title": "Major Technical Issue / Lost Comms", "Options":["Yes", "No"], "Name": "TechnicalIssues"}, 

        {"Type":"TextInput", "Title": "Comments", "Placeholder": "Type here", "Name": "Comments"}]
    HTML = r"""<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">   <title>Match Scouting</title>    <link href="/css/scouting.css" type="text/css" rel="stylesheet"></head><body style="">    <header>        <h1>Match Scouting</h1>        <h2>You are scouting Team {{teamNumber}} on Match {{matchNumber}}.</h2>    </header>    <form method="POST" onsubmit="return confirm(&#39;Are you sure you want to submit the data?&#39;);">"""
    EndHTML = """<input type="submit" value="Submit!">    </form>    <script type="text/javascript" src="/js/numberField.js"></script></body></html>"""
    textToFunction = {"ShortTextInput": makeShortTextInput, "Header": makeHeader, "Options": makeOptions, "Number": makeNumber, "TextInput": makeTextInput}
    for element in data:
        HTML+=textToFunction[element["Type"]](element)
    HTML+=EndHTML
    return HTML


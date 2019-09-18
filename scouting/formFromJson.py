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
        {"Type":"Number", "Title":"Cargo Ship (C)", "Min": '0', "Max": '10', "Name": "SCSC"}, 
        {"Type":"Number", "Title":"Rocket L1 (C)", "Min": '0', "Max": '10', "Name": "SL1C"}, 
        {"Type":"Number", "Title":"Rocket L2 (C)", "Min": '0', "Max": '10', "Name": "SL2C"},
        {"Type":"Number", "Title":"Rocket L3 (C)", "Min": '0', "Max": '10', "Name": "SL3C"},
        {"Type":"Number", "Title":"Cargo Dropped", "Min": '0', "Max": '10', "Name": "SDC"},

        {"Type":"Number", "Title":"Cargo Ship (H)", "Min": '0', "Max": '10', "Name": "SCSH"}, 
        {"Type":"Number", "Title":"Rocket L1 (H)", "Min": '0', "Max": '10', "Name": "SL1H"}, 
        {"Type":"Number", "Title":"Rocket L2 (H)", "Min": '0', "Max": '10', "Name": "SL2H"},
        {"Type":"Number", "Title":"Rocket L3 (H)", "Min": '0', "Max": '10', "Name": "SL3H"},
        {"Type":"Number", "Title":"Hatch Dropped", "Min": '0', "Max": '10', "Name": "SDH"},

        {"Type":"Header", "Title": "Teleoperated Period"}, 
        {"Type":"Number", "Title":"Cargo Ship (C)", "Min": '0', "Max": '10', "Name": "TCSC"}, 
        {"Type":"Number", "Title":"Rocket L1 (C)", "Min": '0', "Max": '10', "Name": "TL1C"}, 
        {"Type":"Number", "Title":"Rocket L2 (C)", "Min": '0', "Max": '10', "Name": "TL2C"},
        {"Type":"Number", "Title":"Rocket L3 (C)", "Min": '0', "Max": '10', "Name": "TL3C"},
        {"Type":"Number", "Title":"Cargo Dropped", "Min": '0', "Max": '10', "Name": "TDC"},

        {"Type":"Number", "Title":"Cargo Ship (H)", "Min": '0', "Max": '10', "Name": "TCSH"}, 
        {"Type":"Number", "Title":"Rocket L1 (H)", "Min": '0', "Max": '10', "Name": "TL1H"}, 
        {"Type":"Number", "Title":"Rocket L2 (H)", "Min": '0', "Max": '10', "Name": "TL2H"},
        {"Type":"Number", "Title":"Rocket L3 (H)", "Min": '0', "Max": '10', "Name": "TL3H"},
        {"Type":"Number", "Title":"Hatches Dropped", "Min": '0', "Max": '10', "Name": "TDH"},

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


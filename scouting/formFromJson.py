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
    data=[{"Type": "ShortTextInput", "Title":"Scouter's Name","Placeholder": "Type here", "DefaultName": "", "Name": "1"}, 
        {"Type":"Header", "Title": "Sandstorm"}, 
        {"Type":"Options", "Title": "Sandstorm Strat", "Options":["Fail", "Not Fail", "kinda fail"], "Name": "3"}, 
        {"Type":"Number", "Title":"Num", "Min": '0', "Max": '10', "Name": "4"}, 
        {"Type":"TextInput", "Title": "Blah", "Placeholder": "Type here", "Name": "5"}]
    HTML = r"""<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">   <title>Match Scouting</title>    <link href="/css/scouting.css" type="text/css" rel="stylesheet"></head><body style="">    <header>        <h1>Match Scouting</h1>        <h2>You are scouting Team {{teamNumber}} on Match {{matchNumber}}.</h2>    </header>    <form method="POST" onsubmit="return confirm(&#39;Are you sure you want to submit the data?&#39;);">"""
    EndHTML = """<input type="submit" value="Submit!">    </form>    <script type="text/javascript" src="/js/numberField.js"></script></body></html>"""
    textToFunction = {"ShortTextInput": makeShortTextInput, "Header": makeHeader, "Options": makeOptions, "Number": makeNumber, "TextInput": makeTextInput}
    for element in data:
        HTML+=textToFunction[element["Type"]](element)
    HTML+=EndHTML
    return HTML


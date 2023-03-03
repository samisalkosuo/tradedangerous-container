#TODO: Flask web app
#https://flask.palletsprojects.com/en/2.2.x/quickstart/#a-minimal-application

#simple web ui
#optoins from environment (can be overridden)
#new options added
import subprocess
import os
from threading import Thread
from time import sleep
import time
from datetime import datetime
import logging

from flask import Flask
from flask import render_template
from flask import abort, redirect, url_for
from flask import request
from . import ExtractOpts

app = Flask(__name__)

#set logging level
app.logger.setLevel(logging.DEBUG)

tradeCommand = "run"

helpFileName = "trade-help.txt"
#get trade help
cmd_str = "trade %s --help > %s" % (tradeCommand, helpFileName)
subprocess.run(cmd_str, shell=True)

if os.path.isfile(helpFileName):
    with open(helpFileName) as file:
        helpText = file.read()
# print(helpText)
# helpText = helpText.split("\n")
# helpText = "<br/>".join(helpText)
findInProgress = False
showHelp = True
options = ExtractOpts.getOptionsFromEnv()

#trade task start/end timestampe
tradeTaskStartTime = None
tradeTaskStartTimestamp = time.time()

def findTradeTask(options):
    global tradeTaskStartTime
    global tradeTaskStartTimestamp
    tradeTaskStartTimestamp = int(time.time())
    tradeTaskStartTime = datetime.now()
    app.logger.debug(f"Start: {tradeTaskStartTime.isoformat()}")
    app.logger.debug(f"Received options: {options}")
    sleep(3)
    #call trade process
    
    resultFileName = f"traderesult-{time.time()}.txt"
    f = open(resultFileName, "w")
    f.write("===================\n")
    f.write(f"{tradeTaskStartTime.isoformat()}\n")
    f.write(f"trade {tradeCommand} {options}\n\n")    
    f.close()
    #execute trade
    cmd_str = f"trade {tradeCommand} {options} >> {resultFileName}"
    subprocess.run(cmd_str, shell=True)

    global findInProgress
    findInProgress = False    
    tradeTaskEndTime = datetime.now()

    app.logger.debug(f"End: {tradeTaskEndTime.isoformat()}")

    app.logger.debug('Execute trade complete.')


def getTradeResults():
    #get all trade-*.txt files and output
    files = []
    for file in os.listdir("."):
        if file.startswith("traderesult"):
            files.append(file)
    files.sort(reverse=True)
    results = []
    for file in files:
        f = open(file)
        for line in f:
            results.append(line.strip())
        f.close()
    return "<br/>\n".join(results)    

@app.route("/")
def index_html():
    global findInProgress
    global options

    opts = options
    cssUrl = url_for('static', filename='style.css')
    tradeResults = getTradeResults()
    return render_template('index.html', 
                           cssUrl = cssUrl,
                           optsString=opts, 
                           findInProgress=findInProgress,
                           helpText=helpText,
                           showHelp=showHelp,
                           tradeTaskStartTimestamp=tradeTaskStartTimestamp,
                           tradeTaskSinceStart=(int(time.time()) - tradeTaskStartTimestamp),
                           tradeTaskStartTime=tradeTaskStartTime,
                           tradeResults=tradeResults)

@app.route("/trade")
def trade_html():
    global findInProgress
    global options

    args = request.args
    optionsRequest = args.get('opts')
    #fromOption = f"\"{args.get('from')}\""
    fromOption = args.get('from')
    
    app.logger.debug(f"options: {options}")
    app.logger.debug(f"fromOption: {fromOption}")
    if optionsRequest != None:
        #remove newlines and extra whitespaces
        optionsList = optionsRequest.splitlines()
        optionsRequest = " ".join(optionsList).strip()
        if fromOption != None and len(fromOption) > 0:
            if "--from" in optionsRequest:
                #remove --from from optionsstring => overried with text field value
                optionsList = optionsRequest.split(" ")
                ind = optionsList.index("--from")
                optionsList.pop(ind + 1)
                optionsList.remove("--from")
                optionsRequest = " ".join(optionsList).strip()
            options = optionsRequest + " --from \"" + fromOption +"\""
        else:
            options = optionsRequest
        if findInProgress == False:
            #get args
            #start thread to call trade command
            thread = Thread(target=findTradeTask, args = [options])
            thread.start()
            findInProgress = True
    return redirect(url_for('index_html'))

@app.route("/toggle-help")
def toggleHelp():
    global showHelp
    showHelp = not showHelp
    return redirect(url_for('index_html'))

#clear displayed results
@app.route("/clear-results")
def removeResults():
    for file in os.listdir("."):
        if file.startswith("traderesult"):
            os.remove(file)
    return redirect(url_for('index_html'))



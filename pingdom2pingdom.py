#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import abort
from flask import make_response
import requests
import json
import os

app = Flask(__name__)

try:
    SCOUTAPP_APIKEY=os.environ['SCOUTAPP_APIKEY']
    app.logger.debug("Scoutapp API key found in env variable")
except:
    SCOUTAPP_APIKEY=False
    app.logger.error("No scoutapp API key found")
    abort(502)

def create_scoutapp_marker(marker_message):
    scoutapp_marker_url = "https://scoutapp.com/api/v2/%s/markers" % SCOUTAPP_APIKEY
    payload = { "notes": marker_message}
    headers = { "Content-Type": "application/json"}
    r = requests.post(scoutapp_marker_url, headers=headers, data=json.dumps(payload))
    if r.status_code == 200:
        return "OK", 200
    else:
        app.logger.debug(r.content)
        return "NOK", 400

@app.route("/monitoring/health", methods=['GET'])
def health():
    if SCOUTAPP_APIKEY:
    	resp = make_response(json.dumps({ "scout_key" : True }), 200)
    else:
    	resp = make_response(json.dumps({ "scout_key" : False }), 502) 
    resp.headers['Content-Type'] = "application/json"
    return resp

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        try:
            pingdom_data = request.get_json()
        except Exception as e:
            app.logger.error("Impossible to extract data from this pingdom call")
            app.logger.error(e)

        try:
            check_name = pingdom_data['check_name']
        except Exception as e:
            app.logger.error("Impossible to extract check_name from this pingdom call")
            app.logger.error(e)
            app.logger.debug(pingdom_data)
        
        try:
            status = pingdom_data['current_state']
        except Exception as e:
            app.logger.error("Impossible to extract status from this pingdom call")
            app.logger.error(e)
            app.logger.debug(pingdom_data)

        marker_message = "%s is %s" % (check_name, status)
        app.logger.debug("Marker message: %s" % marker_message)
        return create_scoutapp_marker(marker_message)
    else:
        return "pingdom2pingdom : pingdom alerts to pingdom markers webhkook !"

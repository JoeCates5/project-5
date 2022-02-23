"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

import pymongo
from pymongo import MongoClient
import os


###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

###
# Pages
###
@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")


    km = request.args.get('km', 999, type=float)
    distance = request.args.get('distance', 999, type=int)
    begin_date = request.args.get('begin_date')



    app.logger.debug("km={}".format(km))
    app.logger.debug("distance={}".format(distance))
    app.logger.debug("begin_date={}".format(begin_date))
    app.logger.debug("request.args: {}".format(request.args))
    # FIXME!
    # Right now, only the current time is passed as the start time
    # and control distance is fixed to 200
    # You should get these from the webpage!
    open_time = acp_times.open_time(km, distance, arrow.get(begin_date)).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, distance, arrow.get(begin_date)).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

@app.route("/submit", methods=['POST'])
def submit():
    if(not request):
        #request contains no data
        return flask.Response(status=204)
    if(request.form['checkpoints'] == []):
        #request contains checkpoints to store
        return flask.Response(status=204)
    else:

        data = {
        'dist': request.form['dist'],
        'start': request.form['start'],
        'checkpoints': request.form['checkpoints']
        }
        client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
        brevetDB = client.brevetDB
        itemId = brevetDB.posts.insert_one(data)
        client.close()
        return flask.Response(status=200)

@app.route("/display")
def display():
    client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
    if(not client):
        #cant connect to the client
        return flask.jsonify(status=500, brevets={"dist": "", "start": "", "checkpoints": ""})

    brevetDB = client.brevetDB
    data = brevetDB.posts.find_one(sort=[('_id', pymongo.DESCENDING)])
    if(not data):
        #we do not have any data
        return flask.jsonify(status=204, brevets={"dist": "", "start": "", "checkpoints": ""})

    dist = data["dist"]
    start = data["start"]
    checkpoints = data["checkpoints"]

    client.close()
    return flask.jsonify(status=200, brevets={"dist": dist, "start": start, "checkpoints": checkpoints})
#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")

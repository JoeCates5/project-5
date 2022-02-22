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

import os
import pymongo
from pymongo import MongoClient

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

###
# Pages
###

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)


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

@app.route("/_submit", methods=['POST'])
def _submit():
    if(not request):
        return flask.Response(status=403)
    elif(request.args.get('checkpoint') == []):
        return flask.Response(status=403)
    else:
        data = {
        'dist': request.args.get('dist'),
        'start': request.args.get('start'),
        'checkpoint': request.args.get('checkpoint')
        }
        brevetDB = client.brevetDB
        brevetDB.posts.insert_one(data)
        brevetDB.close
        return flask.Response(status=200)

@app.route("/_display")
def _display():
    client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
    if(not client):
        return flask.jsonify({"start":'', "dist":'', "checkpoints":''})

    brevetDB = client.brevetDB
    data = mydb.posts.find_one(sort=[('_id', pymongo.DESCENDING)])

    if(not data):
        return flask.jsonify({"start":'', "dist":'', "checkpoints":''})

    dist = data[dist]
    start = data[start]
    checkpoints = data[checkpoints]

    return flask.jsonify({"start":start, "dist":dist, "checkpoints":checkpoints})



#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.DEBUG, host="0.0.0.0")

# Import the dependencies.
from flask import Flask,jsonify
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Stations = Base.classes.station
Measurements = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():

    return """
 <ul>
        <li>/api/v1.0/precipitation</li>
        <li>/api/v1.0/stations</li>
        <li>/api/v1.0/tobs</li>
        <li>/api/v1.0/{start}</li>
        <li>/api/v1.0/{start}/{end}</li>
    </ul>
"""
@app.route("/api/v1.0/precipitation")
def prcp():

    session.close()
    return "prcp"

@app.route("/api/v1.0/stations")
def stations():
    
    session.close()
    return "stations"

@app.route("/api/v1.0/tobs")
def tobs():

    session.close()
    return "tobs"

@app.route("/api/v1.0/<start>")
def start_date(start):

    session.close()
    return start

@app.route("/api/v1.0/<start>/<end>")
def end_date(start,end):
    
    session.close()
    return [start,end]


if __name__ == "__main__":
    app.run(debug=True)
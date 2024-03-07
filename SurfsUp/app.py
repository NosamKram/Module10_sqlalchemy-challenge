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
 # create session link from python to DB
    session=Session(engine)
    """Return a list of precipitation and date for one year"""
    # Calculate the date one year from the last date in data set.
    yearago_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # print(yearago_date)

    # Perform a query to retrieve the data and precipitation scores
    results=session.query(Measurements.date, Measurements.prcp).order_by(Measurements.date.asc()).filter(Measurements.date>=yearago_date).all()
    session.close()
        # Convert list of tuples into dictionary
    precipitation=[]
    for date,prcp in results:
        precipitation_dict={}
        precipitation_dict['date']=date
        precipitation_dict['prcp']=prcp
        precipitation.append(precipitation_dict)
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # create session
    session=Session(engine)
    """Return a list of all stations"""
    # query all stations
    station_result=session.query(Stations.station, Stations.name).all()

    session.close()
    All=[]
    for station, name in station_result:
        Dict_stat={}
        Dict_stat['station']=station
        Dict_stat['name']=name
        All.append(Dict_stat)
    
    return jsonify(All)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Determine the most active station ID
    most_active_station_id = session.query(Measurements.station).\
                             group_by(Measurements.station).\
                             order_by(func.count(Measurements.station).desc()).\
                             first()[0]

    # Find the most recent date and calculate one year ago
    most_recent_date = session.query(func.max(Measurements.date)).scalar()
    most_recent_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d')
    one_year_ago = most_recent_date - dt.timedelta(days=365)

    # Query the last 12 months of TOBS data for the most active station
    results = session.query(Measurements.date, Measurements.tobs).\
        filter(Measurements.station == most_active_station_id).\
        filter(Measurements.date >= one_year_ago).all()
    session.close()

    # Convert to list of dictionaries
    tobs_list = [{"date": date, "tobs": tobs} for date, tobs in results]
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # create session
    session=Session(engine)

    # Calculate the date one year from the last date in data set.
    yearago_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temp_yrago=session.query(func.min(Measurements.tobs), func.max(Measurements.tobs),func.avg(Measurements.tobs)).\
                        filter(Measurements.date >=yearago_date).all()
    session.close()

    tobs_obs={}
    tobs_obs["Min Temp"]=temp_yrago[0][0]
    tobs_obs["Avg Temp"]=temp_yrago[0][1]
    tobs_obs["Max Temp"]=temp_yrago[0][2]
    return jsonify(tobs_obs)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query to find minimum, average, and maximum temps from start_date to end_date
    query_result = session.query(func.min(Measurements.tobs),func.avg(Measurements.tobs),func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).\
        filter(Measurements.date <= end).all()
    
    session.close()

    temp_stats = []
    for min,avg,max in query_result:
        temp_stat_dict = {}
        temp_stat_dict["Minimum"] = min
        temp_stat_dict["Average"] = avg
        temp_stat_dict["Maximum"] = max
        temp_stats.append(temp_stat_dict)

    return jsonify(temp_stats)



if __name__ == "__main__":
    app.run(debug=True)
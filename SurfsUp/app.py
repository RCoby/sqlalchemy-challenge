import numpy as np
import datetime as dt
from datetime import datetime, timedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify

#db setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite",echo=False)

#refelect db
Base=automap_base()
#refelct tables
Base.prepare(autoload_with=engine)

#set ref to table
Station = Base.classes.station
Measurement = Base.classes.measurement

#Create app
app = Flask(__name__)


#API Static Routes
# 1. List available routes.
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    ) 


#2. Convert the query results to a dictionary by using date as the key and prcp as the value & Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    #open db session
    session = Session(engine)

    results=session.query(Measurement.date,Measurement.prcp).all()
    session.close()

    # Create dictionary
    all_precipitation = []
    for date, prcp, in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


#3. Return a JSON list of stations
@app.route("/api/v1.0/stations")
def stations():
    #open db session
    session = Session(engine)
    #query all stations
    results=session.query(Station.station).all()
    session.close()

    #convert tuple to list
    all_stations=list(np.ravel(results))

    return jsonify(all_stations)


#4. Query the dates and temperature observations of the most-active station for the previous year of data & Return a JSON list of temperature observations for the previous year.

@app.route("/api/v1.0/tobs")
def tobs():
    #open db session
    session = Session(engine)
    
    #query date & temp 
    last_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    last_12mths=(dt.datetime.strptime(last_date,'%Y-%m-%d')-timedelta(days=365)).strftime('%Y-%m-%d')
    
    #query most active station
    station_activity=session.query(Measurement.station,func.count(Measurement.station))\
    .group_by(Measurement.station)\
    .order_by(func.count(Measurement.station).desc())\
    .first()[0]
  
    results=session.query(Measurement.date,Measurement.tobs)\
        .filter(Measurement.station==station_activity)\
        .filter(Measurement.date>=last_12mths)\
        .all()
    
    session.close()


    #convert tuple to list
    active_station=list(np.ravel(results))

    return jsonify(active_station)


#5.API Dynamic Route
#i. Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
#ii. For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
#iii. For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive. 

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def date_daterange(start, end=None):
    """fetch Min/Max/Avg for the date/date range the user inputs"""
    #open db session
    session = Session(engine)

    # convert start and end dates to datetime objects
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d") if end else None


    query = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date)

    if end_date:
        query = query.filter(Measurement.date <= end_date)

    values = query.all()
    session.close()

    result = []
    for tmin, tavg, tmax in values:
        result.append({'TMIN': tmin, 'TAVG': round(tavg, 2), 'TMAX': tmax})
        return jsonify(result)
     
    return jsonify({"error": f"The date {start} was not found."}), 404
       


if __name__ == "__main__":
    app.run(debug=True)
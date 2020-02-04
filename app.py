## in terminal, run python app.py

import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)


from flask import Flask, jsonify

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route('/')
def welcome():
    return (
        f"Welcome to the Hawaii Climate App!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

####    return '/api/v1.0/precipitation, /api/v1.0/stations, /api/v1.0/tobs, /api/v1.0/ENTER_START_DATE, /api/v1.0/ENTER_START/END_DATE'   

### /api/v1.0/precipitation - Convert the query results to a Dictionary using date as the key and prcp as the value.

@app.route('/api/v1.0/precipitation')
def precipitation():
    date_1_yr_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= date_1_yr_ago).all()
    precipt = {date: prcp for date, prcp in precipitation}
    return jsonify(precipt)


### /api/v1.0/stations - Return a JSON list of stations from the dataset.
@app.route('/api/v1.0/stations')
def stations():
    results = session.query(Station.station).all()
    station = list(np.ravel(results))
    return jsonify(station)
    

@app.route('/api/v1.0/tobs')
def tobs():
     date_1_yr_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

     results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= date_1_yr_ago).all()

     temp_obsv = list(np.ravel(results))
     return jsonify(temp_obsv)


@app.route('/api/v1.0/temp/<start>')
@app.route('/api/v1.0/temp/<start>/<end>')
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
            results = session.query(*sel).filter(Measurement.date >= start).all()
                
            temps = list(np.ravel(results))
            return jsonify(temps)
        
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    temps = list(np.ravel(results))
    return jsonify(temps)
    
if __name__ == '__main__':
    app.run(debug=True)

#2016-08-23
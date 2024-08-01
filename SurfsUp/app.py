from flask import Flask, jsonify
import datetime as dt
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, scoped_session, sessionmaker

#################################################
# Database Setup
#################################################
# Create an engine to connect to the SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the existing database into a new model
Base = automap_base()
# Reflect the tables using the new autoload_with parameter
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a scoped session factory to manage sessions
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Flask Setup
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Home route
@app.route("/")
def home():
    return (
        f"(Welcome to SQLAlchemy Challenge - Climate App). <br><br>"
        f"Available Routes: <br>"
        
        f"/api/v1.0/precipitation<br/>"
        f"Returns dates and temperature from the last year in data set. <br><br>"
        
        f"/api/v1.0/stations<br/>"
        f"Returns a list of stations. <br><br>"
        
        f"/api/v1.0/tobs<br/>"
        f"Returns list of Temperature Observations for last year in data set. <br><br>"
        
        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"Returns an Average, Max, and Min temperatures for a given start date.<br><br>"
        
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
        f"Returns an Average, Max, and Min temperatures for a given date range."
    )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create a new session
    session = Session()
    try:
        # Query the latest date in the dataset
        latest_date = session.query(func.max(Measurement.date)).scalar()
        # Calculate the date one year ago from the last date
        query_date = (pd.to_datetime(latest_date) - pd.DateOffset(years=1)).strftime("%Y-%m-%d")
        # Query for the last 12 months of precipitation data
        results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()
        # Convert the query results to a dictionary
        precipitation_data = {date: prcp for date, prcp in results}
    finally:
        # Close the session
        session.close()
    
    return jsonify(precipitation_data)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create a new session
    session = Session()
    try:
        # Query all the stations
        results = session.query(Station.station).all()
        # Convert the query results to a list
        stations = [station[0] for station in results]
    finally:
        # Close the session
        session.close()
    
    return jsonify(stations)

# Temperature observations route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create a new session
    session = Session()
    try:
        # Query the latest date in the dataset
        latest_date = session.query(func.max(Measurement.date)).scalar()
        # Calculate the date one year ago from the last date
        query_date = (pd.to_datetime(latest_date) - pd.DateOffset(years=1)).strftime("%Y-%m-%d")
        # Query for the last 12 months of temperature data for the most active station
        most_active_station = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()[0]
        results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station).filter(Measurement.date >= query_date).all()
        # Convert the query results to a list of dictionaries
        temperature_data = [{date: tobs} for date, tobs in results]
    finally:
        # Close the session
        session.close()
    
    return jsonify(temperature_data)

# Route for temperature stats from a given start date
@app.route('/api/v1.0/<date>/')
def given_date(date):
    # Create a new session
    session = Session()
    try:
        # Query the latest date in the dataset
        latest_date = session.query(func.max(Measurement.date)).scalar()
        
        # Handle case where date is not in the correct format
        try:
            dt.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
        
        # Query for the average, max, and min temperatures from the given start date to the latest date
        results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).filter(Measurement.date >= date, Measurement.date <= latest_date).all()
        
        # Convert the query results to a list of dictionaries
        date_list = []
        for result in results:
            row = {
                'Start Date': date,
                'End Date': '2017-08-23', # Based on the latestdate.py of dataset
                'Average Temp': float(result[0]),
                'Highest Temp': float(result[1]),
                'Lowest Temp': float(result[2])
            }
            date_list.append(row)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Close the session
        session.close()
    
    return jsonify(date_list)

# Route for temperature stats from a given start date to an end date
@app.route('/api/v1.0/<start_date>/<end_date>/')
def query_dates(start_date, end_date):
    # Create a new session
    session = Session()
    try:
        # Query for the average, max, and min temperatures between the start and end dates
        results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
        # Convert the query results to a list of dictionaries
        range_list = []
        for result in results:
            row = {
                'Start Date': start_date,
                'End Date': end_date,
                'Average Temp': float(result[0]),
                'Highest Temp': float(result[1]),
                'Lowest Temp': float(result[2])
            }
            range_list.append(row)
    finally:
        # Close the session
        session.close()
    
    return jsonify(range_list)

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)

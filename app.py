#########################################################################################
# SQLAlchemy and Flask Challenge - Surfs Up!
# Submitted by : Sheetal Bongale | UT Data Analysis and Visualization | Feb 15, 2020
# This script will return JSONified query results from API endpoints and 
# serve the queries with Flask. 
#########################################################################################
from flask import Flask , jsonify
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement

Station = Base.classes.station

# Create session
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def Home():
    """List all available api routes."""
    return (
        f"Welcome to Surf's Up! Hawai'i Climate API!<br/>"
        f"______________________________________________<br/>"
        f"Available Routes -<br/>"
        f"List of stations from the dataset:<br/>"
        f"/api/v1.0/stations<br/>"
        f"The precipitation observations for the previous year:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"List of Temperature Observations (tobs) for the previous year:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"______________________________________________<br/>"
        f"Records for the minimum, average and the maximum temperatures for a given start date (year-month-date):<br/>"
        f"/api/v1.0/<start><br/>"
        f"Records for the minimum, average and the maximum temperatures for a given start and end date (year-month-date):<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"______________________________________________<br/>"
    )

def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# Calculate the date 1 year ago from the last data point in the database
last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
last_date = dt.datetime.strptime(last_date, "%Y-%m-%d")
last_year = last_date - dt.timedelta(days=365)

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a dictionary in JSON format where the date is the key and the value is 
    the precipitation data"""

    # Perform a query to retrieve the data and precipitation scores
    prcp_results = ( 
        session.query(Measurement.date, Measurement.prcp)
        .filter(Measurement.date > last_year)
        .order_by(Measurement.date)
        .all()
    )
    # Save the query results as a dictionary with the date as the key and the prcp record as the value
    # Return converted JSON
    return jsonify(dict(prcp_results))

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations"""
    stations_results = session.query(Station.station).all()

    return jsonify(dict(stations_results))

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a JSON list of temperature observations for the previous year"""
    temp_results = (
        session.query(Measurement.date, Measurement.tobs)
        .filter(Measurement.date > last_year)
        .order_by(Measurement.date)
        .all()
    )
    return jsonify(dict(temp_results))

@app.route("/api/v1.0/<start>")
def start(start):
    """Returns the JSON list of the minimum, average and the maximum temperatures for a given start date (year-month-date)"""
    temps = calc_temps(start, last_date)

    # Create a list to store the temperature records
    temp_list = []
    date_dict = {'start_date': start, 'end_date': last_date}
    temp_list.append(date_dict)
    temp_list.append({'Observation': 'Min', 'Temperature': temps[0][0]})
    temp_list.append({'Observation': 'Avg', 'Temperature': temps[0][1]})
    temp_list.append({'Observation': 'Max', 'Temperature': temps[0][2]})

    return jsonify(temp_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    """Returns the JSON list of the minimum, average and the maximum temperatures for a given start date and end date(year-month-date)"""

    temps = calc_temps(start, end)

    # Create a list to store the temperature records
    temp_list = []
    date_dict = {'start_date': start, 'end_date': end}
    temp_list.append(date_dict)
    temp_list.append({'Observation': 'Min', 'Temperature': temps[0][0]})
    temp_list.append({'Observation': 'Avg', 'Temperature': temps[0][1]})
    temp_list.append({'Observation': 'Max', 'Temperature': temps[0][2]})

    return jsonify(temp_list)

#################################################
# Run the application
#################################################
if __name__ == '__main__':
    app.run(debug=True)
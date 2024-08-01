# sqlalchemy-challenge
## Overview
This project involves performing climate data analysis using Python, SQLAlchemy, Pandas, and Matplotlib, followed by creating a Flask API to serve the results of the analysis.

## Files Included
app.py: A Flask web application that provides several API endpoints to interact with the climate data stored in an SQLite database.
climate_starter.ipynb: A Jupyter Notebook for exploratory data analysis (EDA) on the climate data, including loading, cleaning, and visualizing the data.
hawaii.sqlite: The SQLite database containing climate data for Hawaii.
hawaii_measurements.csv: CSV file containing measurement data.
hawaii_stations.csv: CSV file containing station data.

# Project Structure
## Part 1: Analyze and Explore the Climate Data

### Precipitation Analysis
1. Connect to the SQLite database using SQLAlchemy create_engine().
2. Reflect the database tables using automap_base().
3. Create a session to link Python to the database.
4. Find the most recent date in the dataset.
5. Query the previous 12 months of precipitation data.
6. Load the query results into a Pandas DataFrame and set column names.
7. Sort the DataFrame by date and plot the results.
8. Print summary statistics for the precipitation data.

### Station Analysis
1. Query the total number of stations in the dataset.
2. Find the most-active stations and determine which station has the most observations.
3. Calculate the lowest, highest, and average temperatures for the most-active station.
4. Query the previous 12 months of temperature observation (TOBS) data for the most-active station.
5. Plot the TOBS data as a histogram with bins=12.
6. Close the session.


## Part 2: Design Your Climate App
Flask API Routes
Home Route: /
Lists all available API routes.

Precipitation Route: /api/v1.0/precipitation
Returns JSON with date as the key and precipitation as the value.

Stations Route: /api/v1.0/stations
Returns a JSON list of all stations.

TOBS Route: /api/v1.0/tobs
Returns a JSON list of temperature observations for the previous year for the most-active station.

Temperature Stats Routes: /api/v1.0/<start> and /api/v1.0/<start>/<end>
Returns a JSON list of the minimum, average, and maximum temperatures for a specified start or start-end range.

# Conclusion
Through this project, I performed a comprehensive analysis of climate data for Hawaii, covering both precipitation and temperature observations. The analysis revealed valuable insights such as trends in precipitation over the last 12 months and the activity levels of various weather stations. By developing a Flask API, we made this data easily accessible and reusable for further analysis and application development. The combination of Python, SQLAlchemy, Pandas, and Matplotlib provided a robust framework for handling, analyzing, and visualizing the data, while Flask enabled the creation of a user-friendly interface to interact with the results.


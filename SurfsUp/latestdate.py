from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

# Create an engine to connect to the SQLite database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session
session = Session(engine)

# Query the latest date in the Measurement table
latest_date = session.query(func.max(Measurement.date)).scalar()

# Close the session
session.close()

print(f"The latest date in the dataset is: {latest_date}")

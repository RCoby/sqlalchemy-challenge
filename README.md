# sqlalchemy-challenge


## Climate analysis of Honolulu, Hawaii

Perform data modelling, data engineering, and data analysis using the 6 tables in the csv files provided in the data folder.

-----

## Part 1: Analyse and Explore Data
Use Python and SQLAlchemy to do a basic climate analysis and data exploration of climate database

### Precipitation Analysis 
SQLAlchemy ORM queries, Pandas, and Matplotlib

+ Find most recent date in the dataset
+ Collect previous 12 months of precipitation data 
+ Store results in Pandas DataFrame
+ Plot the results

### Station Analysis

+ Determine station count
+ Find most acvtive station by station observations
+ Collect previous 12 months of temperature observation data for most active station
+ Store results in Pandas DataFrame
+ Plot results as a histogram

-----

## Part 2: Design Climate App
Design a Flask API based on the queries 

### API Static Routes
+ precipitation route - list date and precipitation value
+ stations route - list stations in database
+ tobs route - most active staion 

### API Dynamic Route
List min, max, and average temperatures:
+ start route - from user set start date to end of dataset
+ start/end route - from user set start date and end date


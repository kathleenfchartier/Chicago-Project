# IMPORT THE SQALCHEMY LIBRARY's CREATE_ENGINE METHOD
import sqlalchemy
import pymysql
import mysql
import pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import StrMethodFormatter
import matplotlib.ticker as ticker
import matplotlib as mpl


# DEFINE THE DATABASE CREDENTIALS
user = 'root'
password = 'Just4You'
host = 'localhost'
port = 3306
database = 'Chicago_data'

# PYTHON FUNCTION TO CONNECT TO THE MYSQL DATABASE AND
# RETURN THE SQLACHEMY ENGINE OBJECT
def get_connection():
	return create_engine(
		url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(user, password, host, port, database)
	).connect()

try:
	
# GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE
	engine = get_connection()
	print(
		f"Connection to the {host} for user {user} created successfully.")
except Exception as ex:
		print("Connection could not be made due to the following error: \n", ex)

query=text("select cr.`Community Area`, se.`HARDSHIP INDEX`, count(cr.`ID`) as `crime_count`\
    from chicago_crime_data as cr, chicago_socioeconomic_data as se\
    where cr.`Community Area`=se.`Community Area Number`\
    group by cr.`Community Area` , se.`HARDSHIP INDEX`\
    order by  cr.`Community Area`")

# read table data using sql query
hardship_crime=pd.read_sql_query(query, engine)

hardship_crime.head()



# Setting seaborn as default style even
# if use only matplotlib
sns.set()

# plot Hardship vs crime count
plot1= sns.regplot(x='HARDSHIP INDEX',y='crime_count', 
		   	scatter_kws = {"color": "blue", "alpha": 0.5},
            line_kws = {"color": "blue"},  scatter=True, marker="o", data=hardship_crime)

plot1.get_yaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

#specfiy axis labels
plot1.set(xlabel='Hardship Index', ylabel='Number of Crimes', title='Crimes by Area vs. Hardship Index')
plot1.set_xlim(1, 100)

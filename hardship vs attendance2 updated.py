# IMPORT THE SQALCHEMY LIBRARY's CREATE_ENGINE METHOD
import sqlalchemy
import pymysql
import mysql
import pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


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

query=text("select se.`HARDSHIP INDEX`, \
		       	cast(ps.`Average Student Attendance` as decimal(5,1)) AS `Average Student Attendance`\
				from chicago_public_schools as ps, chicago_socioeconomic_data as se\
				where se.`Community Area Number`=ps.`Community Area Number`")

# read table data using sql query
attendance=pd.read_sql_query(query, engine)

attendance.head()

# Setting seaborn as default style even
# if use only matplotlib
sns.set()

# plot attendance vs. Hardship

plot1= sns.regplot(x='HARDSHIP INDEX',y='Average Student Attendance', 
		   	scatter_kws = {"color": "blue", "alpha": 0.5},
            line_kws = {"color": "blue"},  scatter=True, marker="o", data=attendance.replace(0, np.nan))



#specfiy axis labels
plot1.set(xlabel='Hardship Index', ylabel='Percent Average Student Attendance', title='Average Student Attendance vs. Hardship Index')
plot1.set_xlim(1, 100)
plot1.set_ylim(0, 100)

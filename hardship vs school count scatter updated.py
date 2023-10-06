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


# DEFINE THE DATABASE CREDENTIALS  - acutal login omitted for security purposes
user = 'x'
password = 'x'
host = 'x'
port = x
database = 'x'

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

query=text("select ps.`Elementary, Middle, or High School`, count(ps.`School ID`) as school_count, se.`HARDSHIP INDEX`\
	from chicago_public_schools as ps, chicago_socioeconomic_data as se\
	where ps.`Community Area Number`=se.`Community Area Number`\
	group by se.`HARDSHIP INDEX`, ps.`Elementary, Middle, or High School`;")


# read table data using sql query
hardship_schools=pd.read_sql_query(query, engine)

hardship_schools.head()


# Setting seaborn as default style even
# if use only matplotlib
sns.set()



plot1= sns.scatterplot(x='HARDSHIP INDEX',y='school_count', hue='Elementary, Middle, or High School', 
		        data=hardship_schools.replace(0, np.nan))

plot1.legend_.set_title(None)
plot1.legend(loc="upper left")


#specfiy axis labels
plot1.set(xlabel='Hardship Index', ylabel='Number of Schools', title='Number of School Types vs. Hardship Index')
plot1.set_xlim(0, 100)
plot1.set_ylim(0, 25)

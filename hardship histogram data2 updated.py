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

query=text("select `Hardship Index` from chicago_socioeconomic_data")


# read table data using sql query
hardship=pd.read_sql_query(query, engine)

hardship.head()

# plot Hardship as histogram

# Setting seaborn as default style even
# if use only matplotlib
sns.set()



plt.figure(figsize=(15,8))
plot1= sns.displot(hardship, binwidth=10, legend=False)
plt.ylim(1, 10)


#specfiy axis labels
plot1.set(xlabel='Hardship Index', ylabel='Number of Communities', title='Community Hardship Distribution')

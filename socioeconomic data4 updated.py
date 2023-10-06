#  The socioeconomic data4 python file had to be updated due to sqlalchemy 2.0 release.

# IMPORT THE SQALCHEMY LIBRARY's CREATE_ENGINE METHOD
import sqlalchemy
import pymysql
import mysql
import pandas as pd
from sqlalchemy import create_engine, text   #added text
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import StrMethodFormatter
import matplotlib.ticker as ticker
import matplotlib as mpl


# DEFINE THE DATABASE CREDENTIALS
user = 'x'
password = 'x'
host = 'x'
port = x
database = 'x'


try:
	
# GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE
#  how to use sqlalchemy 2.0  
# https://stackoverflow.com/questions/75309237/read-sql-query-throws-optionengine-object-has-no-attribute-execute-with

	engine=create_engine("mysql+pymysql://root:Just4You@localhost/Chicago_data")

	conn=engine.connect()
	print(
		f"Connection to the {host} for user {user} created successfully.")
except Exception as ex:
		print("Connection could not be made due to the following error: \n", ex)


#create variable for the sql query
query=text("select `Community Area Number`, `PERCENT OF HOUSING CROWDED`,\
	`PERCENT HOUSEHOLDS BELOW POVERTY`, `PERCENT AGED 16+ UNEMPLOYED`,\
	`PERCENT AGED 25+ WITHOUT HIGH SCHOOL DIPLOMA`, `PER CAPITA INCOME`,\
	`HARDSHIP INDEX`\
	from  chicago_socioeconomic_data;")

# read table data using sql query
socioecon=pd.read_sql_query(query, conn)

socioecon.head()

# Setting seaborn as default style even
# if use only matplotlib
sns.set()

# plot Hardship vs socioeconomic data

fig, axs = plt.subplots(2, 2, sharex=True, figsize=(15,8))
fig.suptitle('Socioeconomic Data vs. Hardship Index')

# Without high school diploma
plot1= sns.regplot(ax=axs[0,0], x='HARDSHIP INDEX',y='PERCENT AGED 25+ WITHOUT HIGH SCHOOL DIPLOMA', 
		   	scatter=True,  data=socioecon)
axs[0, 0].set_title("Over Age 25 without HS Diploma")
axs[0, 0].set(xlabel='Hardship Index', ylabel='Percent of Residents')

# Per Capita Income
plot1= sns.regplot(ax=axs[1, 0], x='HARDSHIP INDEX',y='PER CAPITA INCOME', 
		   	label='Income', scatter=True, data=socioecon)
axs[1, 0].set_title("Per Capita Income")
axs[1, 0].set(xlabel='Hardship Index', ylabel='Income ($)')
# Add tick marks for thousands
axs[1, 0].get_yaxis().set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

# Unemployed
plot1= sns.regplot(ax=axs[0,1], x='HARDSHIP INDEX',y='PERCENT AGED 16+ UNEMPLOYED', 
		   	scatter=True,  data=socioecon)
axs[0, 1].set_title("Over Age 16 Unemployed")
axs[0, 1].set(xlabel='Hardship Index', ylabel='Percent of Residents')

# Below poverty
plot1= sns.regplot(ax=axs[1, 1], x='HARDSHIP INDEX',y='PERCENT HOUSEHOLDS BELOW POVERTY', 
		   	scatter=True, data=socioecon)

axs[1, 1].set_title("Households below Poverty")
axs[1, 1].set(xlabel='Hardship Index', ylabel='Percent of Households')

plot1.set_xlim(1, 100)
plot1.set_ylim(1, 100)

fig.tight_layout()

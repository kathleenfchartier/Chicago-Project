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

query=text("select ce.`HARDSHIP INDEX`, \
        cast(ps.`Freshman on Track Rate perc` as decimal(3,1)) as `Freshman on Track`, \
        cast(ps.`9th Grade EXPLORE (2009)` as decimal(3,1)) as `9th Grade Average EXPLORE (2009)`,\
        cast(ps.`9th Grade EXPLORE (2010)` as decimal(3,1)) as `9th Grade Average EXPLORE (2010)`,\
        cast(ps.`10th Grade PLAN (2009)` as decimal(3,1)) as `10th Grade Average PLAN (2009)`,\
        cast(ps.`10th Grade PLAN (2010)` as decimal(3,1)) as `10th Grade Average PLAN (2010)`,\
        cast(ps.`11th Grade Average ACT (2011)` as decimal(3,1)) as `11th Grade Average ACT (2011)`,\
        cast(ps.`Graduation Rate perc` as decimal(3,1)) as `Percent Graduation Rate`,\
        cast(ps.`College Enrollment Rate perc` as decimal(3,1)) as `Percent College Enrollment`\
from chicago_public_schools_perc as ps left join chicago_socioeconomic_data as ce \
on ps.`Community Area Number`=ce.`Community Area Number`\
where `Elementary, Middle, or High School`='HS'\
order by `HARDSHIP INDEX`;")

# read table data using sql query
scores_hs=pd.read_sql_query(query, engine)

scores_hs.head()

# plot Hardship vs scores

# Setting seaborn as default style even
# if use only matplotlib
sns.set()

figure, axes = plt.subplots(1, 2, sharex=True, figsize=(15,8))
figure.suptitle('EXPLORE and PLAN scores vs. Hardship Index')

# Grades 9 student performance
plot1= sns.regplot(ax=axes[0], x='HARDSHIP INDEX',y='9th Grade Average EXPLORE (2009)', 
		   	scatter_kws = {"color": "blue", "alpha": 0.5},
            line_kws = {"color": "blue"}, label='2009', scatter=True, marker="o", data=scores_hs.replace(0, np.nan))
plot1 = sns.regplot(ax=axes[0], x='HARDSHIP INDEX',y='9th Grade Average EXPLORE (2010)',
		    scatter_kws = {"color": "orange", "alpha": 0.5},
            line_kws = {"color": "orange"}, label='2010', scatter=True, marker="s", data=scores_hs.replace(0, np.nan))

#specfiy axis labels
plot1.set(xlabel='Hardship Index', ylabel='Average Score', title='Grade 9 Average EXPLORE Scores')
plot1.set_xlim(1, 100)
plot1.set_ylim(1, 25)
plot1.legend(loc="lower left")

# Grades 10 student performance
plot1= sns.regplot(ax=axes[1], x='HARDSHIP INDEX',y='10th Grade Average PLAN (2009)', 
		   	scatter_kws = {"color": "blue", "alpha": 0.5},
            line_kws = {"color": "blue"}, label='2009', scatter=True, marker="o", data=scores_hs.replace(0, np.nan))
plot1 = sns.regplot(ax=axes[1], x='HARDSHIP INDEX',y='10th Grade Average PLAN (2010)', 
		    scatter_kws = {"color": "orange", "alpha": 0.5},
            line_kws = {"color": "orange"}, label='2010', scatter=True, marker="s", data=scores_hs.replace(0, np.nan))

#specfiy axis labels
plot1.set(xlabel='Hardship Index', ylabel='Average Score', title='Grade 10 Average PLAN Scores')
plot1.set_xlim(1, 100)
plot1.set_ylim(1, 32)
plot1.legend(loc="lower left")

figure, axes = plt.subplots(1, 2, sharex=True, figsize=(15,8))
figure.suptitle('Grades 11-12 Data vs. Hardship Index')

# Grades 11 ACT scores
plot2= sns.regplot(ax=axes[0], x='HARDSHIP INDEX',y='11th Grade Average ACT (2011)', 
		    scatter_kws = {"color": "green", "alpha": 0.5},
            line_kws = {"color": "green"}, scatter=True, marker="o", data=scores_hs.replace(0, np.nan))
#plot2 = sns.regplot(ax=axes[0], x='HARDSHIP INDEX',y='', label='', scatter=True, marker="s", data=scores_hs.replace(0, np.nan))

#specfiy axis labels
plot2.set(xlabel='Hardship Index', ylabel='Average Score', title='Grade 11 Average ACT Scores')
plot2.set_xlim(1, 100)
plot2.set_ylim(1, 36)


# College data
plot2= sns.regplot(ax=axes[1], x='HARDSHIP INDEX',y='Percent Graduation Rate', 
		    scatter_kws = {"color": "purple", "alpha": 0.5},
            line_kws = {"color": "purple"}, label='Graduation', scatter=True, marker="o", data=scores_hs.replace(0, np.nan))
plot2 = sns.regplot(ax=axes[1], x='HARDSHIP INDEX',y='Percent College Enrollment', 
		    scatter_kws = {"color": "red", "alpha": 0.5},
            line_kws = {"color": "red"},
		    label='College Enrollment', scatter=True, marker="s", data=scores_hs.replace(0, np.nan))

#specfiy axis labels
plot2.set(xlabel='Hardship Index', ylabel='Percent of Students', title='Grade 12 Graduation and College Enrollment')
plot2.set_xlim(1, 100)
plot2.set_ylim(1, 100)
plot2.legend(loc="upper right")
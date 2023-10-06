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
        cast(ps.`Pk-2 Literacy perc` as decimal(3,1)) as `Pk-2 Literacy perc`, \
        cast(ps.`Pk-2 Math perc` as decimal(3,1)) as `Pk-2 Math perc`,\
        cast(ps.`Gr3-5 Grade Level Math perc` as decimal(3,1)) as `Gr3-5 Grade Level Math perc`, \
        cast(ps.`Gr3-5 Grade Level Read perc` as decimal(3,1)) as `Gr3-5 Grade Level Read perc`\
from chicago_public_schools_perc as ps left join chicago_socioeconomic_data as ce \
on ps.`Community Area Number`=ce.`Community Area Number`\
where `Elementary, Middle, or High School`='ES'\
order by `HARDSHIP INDEX`")

# read table data using sql query
scores_es=pd.read_sql_query(query, engine)

scores_es.head()

# plot Hardship vs scores

# Setting seaborn as default style even
# if use only matplotlib
sns.set()

figure, axes = plt.subplots(1, 2, sharex=True, figsize=(15,8))
figure.suptitle('Students at Benchmark vs. Hardship Index')


# Pre-k student performance
pk = sns.regplot(ax=axes[0], x='HARDSHIP INDEX',y='Pk-2 Literacy perc', label='Literacy', scatter=True, marker="o", data=scores_es.replace(0, np.nan))
pk = sns.regplot(ax=axes[0], x='HARDSHIP INDEX',y='Pk-2 Math perc', label='Math', scatter=True, marker="s", data=scores_es.replace(0, np.nan))

#specfiy axis labels
pk.set(xlabel='HARDSHIP INDEX', ylabel='Percent of Students ', title='Pre-k to Grade 2')
pk.set_xlim(1, 100)
pk.set_ylim(1, 100)
pk.legend(loc="lower left")

# Gr 3-5 student performance		

gr = sns.regplot(ax=axes[1], x='HARDSHIP INDEX',y='Gr3-5 Grade Level Read perc', label='Literacy', scatter=True, marker="o", data=scores_es.replace(0, np.nan))
gr = sns.regplot(ax=axes[1], x='HARDSHIP INDEX',y='Gr3-5 Grade Level Math perc', label='Math', scatter=True, marker="s", data=scores_es.replace(0, np.nan))

#specfiy axis labels
gr.set(xlabel='Hardship Index', ylabel='Percent of Students', title='Grades 3-5')
gr.set_xlim(1, 100)
gr.set_ylim(1, 100)
gr.legend(loc="lower left")
# IMPORT THE SQALCHEMY LIBRARY's CREATE_ENGINE METHOD
import sqlalchemy
import pymysql
import mysql
import pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

query=text("select ce.`HARDSHIP INDEX`, \
        cast(ps.`Gr6-8 Grade Level Math perc` as decimal(3,1)) as `Gr6-8 Grade Level Math perc`, \
        cast(ps.`Gr6-8 Grade Level Read perc` as decimal(3,1)) as `Gr6-8 Grade Level Read perc`,\
        cast(ps.`Gr-8 Explore Math perc` as decimal(3,1)) as `Gr-8 Explore Math perc`,\
        cast(ps.`Gr-8 Explore Read perc` as decimal(3,1)) as `Gr-8 Explore Read perc`\
from chicago_public_schools_perc as ps left join chicago_socioeconomic_data as ce \
on ps.`Community Area Number`=ce.`Community Area Number`\
where `Elementary, Middle, or High School`='MS'\
order by `HARDSHIP INDEX`;")

# read table data using sql query
scores_ms=pd.read_sql_query(query, engine)

scores_ms.head()

# plot Hardship vs scores

# Setting seaborn as default style even
# if use only matplotlib
sns.set()

figure, axes = plt.subplots(1, 2, sharex=True, figsize=(15,8))
figure.suptitle('Student Benchmarks vs. Hardship Index')

# grades 6-8 student performance
ms1 = sns.regplot(ax=axes[0], x='HARDSHIP INDEX',y='Gr6-8 Grade Level Read perc', label='Literacy', scatter=True, marker="o", data=scores_ms.replace(0, np.nan))
ms1 = sns.regplot(ax=axes[0], x='HARDSHIP INDEX',y='Gr6-8 Grade Level Math perc', label='Math', scatter=True, marker="s", data=scores_ms.replace(0, np.nan))

#specfiy axis labels
ms1.set(xlabel='HARDSHIP INDEX', ylabel='Percent of Students', title='Grades 6-8 at Grade Level')
ms1.set_xlim(1, 100)
ms1.set_ylim(1, 100)
ms1.legend(loc="lower left")

# grades 6-8 student performance	

ms2 = sns.regplot(ax=axes[1], x='HARDSHIP INDEX',y='Gr-8 Explore Read perc', label='Literacy', scatter=True, marker="o", data=scores_ms.replace(0, np.nan))
ms2 = sns.regplot(ax=axes[1], x='HARDSHIP INDEX',y='Gr-8 Explore Math perc', label='Math', scatter=True, marker="s", data=scores_ms.replace(0, np.nan))

#specfiy axis labels
ms2.set(xlabel='Hardship Index', ylabel='Percent of Students', title='Grade 8 College Readiness Benchmark')
ms2.set_xlim(1, 100)
ms2.set_ylim(1, 100)
ms2.legend(loc="lower left")

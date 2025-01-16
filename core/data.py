import pandas as pd
import numpy as np
import json
from django import template
import pickle
import xgboost as xgbl
from django.contrib.staticfiles.finders import find
import os
import pymysql
from sqlalchemy import create_engine, text
import environ

# Envirionment variables
env = environ.Env()
environ.Env.read_env()

# Function replace
register = template.Library()

@register.filter
def replace(value, arg):
    old, new = arg.split(',')
    return value.replace(old, new)

########## Data for the Ecommerce project ############

# Get data from database
mysql_user = env('DB_USER')
mysql_password = env('DB_PASSWORD')
mysql_host = env('DB_HOST')
mysql_db = env('DB_NAME')
mysql_port = env('DB_PORT')

engine = create_engine('postgresql+psycopg2://' + mysql_user + ':' + mysql_password + '@' + mysql_host + ':' + mysql_port + '/' + mysql_db)

try:
    with engine.connect() as connection:

        query = text("select * from test_data_dashboard;")
        
        df = pd.read_sql_query(query, con=connection)
        
except Exception as e:
    print(f"Error collecting data from database : {e}")

# Revenue data
revenue_by_category = {
    "<10 000€": 16.46,
    "<1000€": 16.46,
    "<5000€": 54.43,
    ">20 000€": 12.66,
}

time_series = {
    "dates": ["sept. 2016", "nov. 2016", "janv. 2017", "mars 2017", "mai 2017", "juil. 2017"],
    "revenue": [0, 50000, 70000, 40000, 60000, 100000],
}

# Map JSON
with open(find('js/Europe_countries_shp_custom.json'), 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

for k in range(len(geojson_data['features'])):
    geojson_data['features'][k]['id'] = geojson_data['features'][k]['properties']['ISO3']


########## Data for the Bank Churn rate project ############
cr_data = pd.read_csv(find("data/train.csv"))
cr_cat_variables = ['Geography', 'Gender', 'HasCrCard', 'IsActiveMember', 'NumOfProducts', 'Tenure']
cr_data_describe = pd.concat([cr_data.describe(include='all'), cr_data.isnull().sum(axis=0).to_frame(name="missing_values").T], axis=0).round(2).drop(index=['unique', 'top', 'freq'])
cr_data = cr_data.drop(columns=['Surname', 'CustomerId', 'id'])

with open(find("models/bank_churnrate_xgboost.pkl"), 'rb') as file:  
    model = pickle.load(file)

# Extraire les importances des features
feature_importance = model.get_booster().get_score(importance_type="weight")
importance_df = pd.DataFrame({
    "Feature": list(feature_importance.keys()),
    "Importance": list(feature_importance.values())
}).sort_values(by="Importance", ascending=True)









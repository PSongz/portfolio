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

        query_metrics = text("select * from dashboard_metrics;")
        query_category = text("select * from dashboard_price_category;")
        query_isnew = text("select * from dashboard_isnew;")
        query_date = text("select * from dashboard_date;")
        query_country = text("select * from dashboard_country;")
        
        metrics = pd.read_sql_query(query_metrics, con=connection)
        revenue_by_price_category = pd.read_sql_query(query_category, con=connection)
        revenue_by_isnew = pd.read_sql_query(query_isnew, con=connection)
        revenue_by_date = pd.read_sql_query(query_date, con=connection)
        revenue_by_country = pd.read_sql_query(query_country, con=connection)
        
except Exception as e:
    print(f"Error collecting data from database : {e}")

revenue_by_price_category = revenue_by_price_category[revenue_by_price_category['revenue'] != 0]
revenue_by_price_category['revenue'] = revenue_by_price_category['revenue'].round().astype(int)
revenue_by_isnew['revenue'] = revenue_by_isnew['revenue'].round().astype(int)
revenue_by_isnew['category'] = np.where(revenue_by_isnew['isnew'] == 0, 'New', 'Returning')
revenue_by_date['revenue'] = revenue_by_date['revenue'].round().astype(int)
revenue_by_country['revenue'] = revenue_by_country['revenue'].round().astype(int)

# Map JSON
with open(find('js/Europe_countries_shp_custom.json'), 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

for k in range(len(geojson_data['features'])):
    geojson_data['features'][k]['id'] = geojson_data['features'][k]['properties']['ISO3']


########## Data for the Bank Churn rate project ############
with engine.connect() as connection:

    query = text("select * from banck_churn_train;")
    
    cr_data = pd.read_sql_query(query, con=connection)

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









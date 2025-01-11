import pandas as pd
import numpy as np
import json
from django import template
import pickle
import xgboost as xgbl


# Function replace
register = template.Library()

@register.filter
def replace(value, arg):
    old, new = arg.split(',')
    return value.replace(old, new)

########## Data for the Ecommerce project ############

# Simulated data
data = {
    "country": ["United Kingdom", "Switzerland", "Ukraine", "France", "Germany", "Netherlands"],
    "ISO3": ['GBR', 'CHE', 'UKR', 'FRA', 'DEU', 'NLD'],
    "revenue": [164634, 54632, 44122, 33525, 26152, 25905],
    "visits": [37393, 4427, 5577, 15832, 19980, 11453],
    "conversion_rate": [0.04, 0.2, 0.07, 0.03, 0.03, 0.03],
    "aov": [10290, 670, 11531, 6659, 3269, 8635],
    "bounce_rate": [61, 56, 67, 60, 62, 58],
}

# Storing data in DF
df = pd.DataFrame(data)

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
with open('C:\\Users\\pierr\\django_projects\\portfolio\\Europe_countries_shp_custom.json', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

for k in range(len(geojson_data['features'])):
    geojson_data['features'][k]['id'] = geojson_data['features'][k]['properties']['ISO3']


########## Data for the Bank Churn rate project ############
cr_data = pd.read_csv(r"C:\Users\pierr\django_projects\portfolio\static\data\train.csv")
cr_cat_variables = ['Geography', 'Gender', 'HasCrCard', 'IsActiveMember', 'NumOfProducts', 'Tenure']
cr_data_describe = pd.concat([cr_data.describe(include='all'), cr_data.isnull().sum(axis=0).to_frame(name="missing_values").T], axis=0).round(2).drop(index=['unique', 'top', 'freq'])
cr_data = cr_data.drop(columns=['Surname', 'CustomerId', 'id'])

with open(r"C:\Users\pierr\django_projects\portfolio\static\models\bank_churnrate_xgboost.pkl", 'rb') as file:  
    model = pickle.load(file)

# Extraire les importances des features
feature_importance = model.get_booster().get_score(importance_type="weight")
importance_df = pd.DataFrame({
    "Feature": list(feature_importance.keys()),
    "Importance": list(feature_importance.values())
}).sort_values(by="Importance", ascending=True)









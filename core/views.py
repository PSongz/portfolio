import pandas as pd
import numpy as np
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse
import json
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import seaborn as sns
sns.set_theme()
from plotly.offline import plot
import matplotlib.pyplot as plt
from .data import df, revenue_by_category, time_series, geojson_data, cr_data, cr_cat_variables, cr_data_describe, importance_df, model
from .models import *
from io import BytesIO
import base64

def save_plot_to_html(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    encoded_image = base64.b64encode(image_png).decode("utf-8")
    return f'<img src="data:image/png;base64,{encoded_image}"/>'


class HomeTemplateView(TemplateView):
    template_name = 'home.html'
    
    #override get context date method
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = About.objects.first()
        context['services'] = Service.objects.all()
        context['works'] = RecentWork.objects.all()
        context['clients'] = Client.objects.all()
        return context
        

def BankChurnView(request):
    
    # Descriptive table
    cr_data_describe_html = cr_data_describe.to_html(classes="styled-table")
    
    # colorscale
    cr_palette = px.colors.sequential.Teal
    cr_palette_r = px.colors.sequential.Teal_r
    
    #------------ Charts categorical data ---------------#
    
    cr_plot_country = px.pie(
        cr_data,
        names="Geography", 
        color_discrete_sequence=cr_palette,
)

    cr_plot_country.update_layout(        
        title= {
            'text':"Breakdown of clients by country",        
            'x': 0.5,  # Centre le titre horizontalement (valeurs entre 0 et 1)
            'xanchor': 'center',  # Ancre du titre
            'yanchor': 'top',
            'y': 1
        },
        title_font={
            'size': 26,  # Taille de la police
            'color': 'black',  # Couleur en noir foncé
            'family': 'Arial Bold',  # Police facultative (peut être personnalisée)
        }
)

    cr_plot_gender = px.pie(
        cr_data,
        names="Gender", 
        title="Breakdown of clients by gender",
        color_discrete_sequence=cr_palette,
)

    cr_plot_gender.update_layout(        
        title= {      
            'x': 0.5,  # Centre le titre horizontalement (valeurs entre 0 et 1)
            'xanchor': 'center',  # Ancre du titre
            'yanchor': 'top',
            'y': 1
        },
        title_font={
            'size': 26,  # Taille de la police
            'color': 'black',  # Couleur en noir foncé
            'family': 'Arial Bold',  # Police facultative (peut être personnalisée)
        }
)
    
    cr_plot_cc = px.pie(
        cr_data,
        names="HasCrCard", 
        title="Clients with or without a credit card",
        color_discrete_sequence=cr_palette,
)

    cr_plot_cc.update_layout(        
        title= {      
            'x': 0.5,  # Centre le titre horizontalement (valeurs entre 0 et 1)
            'xanchor': 'center',  # Ancre du titre
            'yanchor': 'top',
            'y': 1
        },
        title_font={
            'size': 26,  # Taille de la police
            'color': 'black',  # Couleur en noir foncé
            'family': 'Arial Bold',  # Police facultative (peut être personnalisée)
        }
)
    
    cr_plot_am = px.pie(
        cr_data,
        names="IsActiveMember", 
        title="Active and inactive clients",
        color_discrete_sequence=cr_palette,
)
    
    cr_plot_am.update_layout(        
        title= {      
            'x': 0.5,  # Centre le titre horizontalement (valeurs entre 0 et 1)
            'xanchor': 'center',  # Ancre du titre
            'yanchor': 'top',
            'y': 1
        },
        title_font={
            'size': 26,  # Taille de la police
            'color': 'black',  # Couleur en noir foncé
            'family': 'Arial Bold',  # Police facultative (peut être personnalisée)
        }
)
    
    cr_plot_exited = px.pie(
        cr_data,
        names="Exited", 
        title="Client exited the bank",
        color_discrete_sequence=cr_palette,
)

    cr_plot_exited.update_layout(        
        title= {      
            'x': 0.5,  # Centre le titre horizontalement (valeurs entre 0 et 1)
            'xanchor': 'center',  # Ancre du titre
            'yanchor': 'top',
            'y': 1
        },
        title_font={
            'size': 26,  # Taille de la police
            'color': 'black',  # Couleur en noir foncé
            'family': 'Arial Bold',  # Police facultative (peut être personnalisée)
        }
)
    
    # Compter les occurrences des valeurs dans les colonnes "Nombre de produit" et "Tenure"
    nbp_counts = cr_data["NumOfProducts"].value_counts().sort_index()
    tenure_counts = cr_data["Tenure"].value_counts().sort_index()

    cr_plot_nbp = px.bar(
        nbp_counts,
        x=nbp_counts.index,
        y=nbp_counts.values, 
        title="Number of products",
        color_discrete_sequence=cr_palette_r,
)
  
    cr_plot_nbp.update_layout(        
        title= {      
            'x': 0.5,  # Centre le titre horizontalement (valeurs entre 0 et 1)
            'xanchor': 'center',  # Ancre du titre
            'yanchor': 'top',
            'y': 1
        },
        title_font={
            'size': 26,  # Taille de la police
            'color': 'black',  # Couleur en noir foncé
            'family': 'Arial Bold',  # Police facultative (peut être personnalisée)
        },
        xaxis_title='',
        yaxis_title=''
)
      
    cr_plot_tenure = px.bar(
        tenure_counts,
        x=tenure_counts.index,
        y=tenure_counts.values, 
        title="Tenure",
        color_discrete_sequence=cr_palette_r,
)

    cr_plot_tenure.update_layout(        
        title= {      
            'x': 0.5,  # Centre le titre horizontalement (valeurs entre 0 et 1)
            'xanchor': 'center',  # Ancre du titre
            'yanchor': 'top',
            'y': 1,
        },
        title_font={
            'size': 26,  # Taille de la police
            'color': 'black',  # Couleur en noir foncé
            'family': 'Arial Bold',  # Police facultative (peut être personnalisée)
        },
        xaxis_title='',
        yaxis_title=''
)
    
    # Convert plots to HTML
    cr_plots = {
        "country": plot(cr_plot_country, output_type="div", include_plotlyjs=False),
        "gender": plot(cr_plot_gender, output_type="div", include_plotlyjs=False),
        "HasCreditCard": plot(cr_plot_cc, output_type="div", include_plotlyjs=False),
        "IsActiveMember": plot(cr_plot_am, output_type="div", include_plotlyjs=False),
        "NumberOfProducts": plot(cr_plot_nbp, output_type="div", include_plotlyjs=False),
        "Tenure": plot(cr_plot_tenure, output_type="div", include_plotlyjs=False),
    }
        
    #------------ Charts categorical data ends ---------------#
    
    #------------ Charts continous data starts ---------------#
    sns.set_palette("crest")
    figs = {}
    for col in ["EstimatedSalary", "Balance", "Age", "CreditScore"]:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(cr_data, x=col, kde=True, ax=ax)
        ax.set_title("")
        ax.set_xlabel("")
        ax.set_ylabel("")
        figs[col] = save_plot_to_html(fig)
        plt.close(fig)


    # Ajouter les graphiques dans un dictionnaire
    cr_plots_continuous = {
        "EstimatedSalary": figs["EstimatedSalary"],
        "Balance": figs["Balance"],
        "Age": figs["Age"],
        "CreditScore": figs["CreditScore"],
    }

    #------------ Charts continous data ends ---------------#
    
    #------------ Correlation matrix ---------------#
    cr_num_variables = cr_data.select_dtypes(include=np.number).columns.tolist()
    cr_plot_heatmap = px.imshow(cr_data[cr_num_variables].corr().round(2), text_auto=True, aspect="auto", color_continuous_scale=px.colors.sequential.Teal)
    
    cr_plot_heatmap.update_layout(
        autosize=True,  # Autorise Plotly à s'adapter au conteneur parent
        margin=dict(l=20, r=20, t=40, b=20),  # Ajuste les marges internes
        height=None,  # Supprime les dimensions explicites pour permettre au CSS de contrôler la hauteur
        width=None    # Supprime les dimensions explicites pour permettre au CSS de contrôler la largeur
)

    #------------ Model's feature importance ---------------#
    cr_plot_fi = px.bar(
        importance_df,
        x="Importance",
        y="Feature",
        orientation="h",  # Barres horizontales
        title="Feature Importance (XGBoost)",
        color="Importance",  # Ajout de couleur
        color_continuous_scale=cr_palette  # Palette de couleurs
)
    cr_plot_fi.update_layout(
        autosize=True,  # Autorise Plotly à s'adapter au conteneur parent
        margin=dict(l=20, r=20, t=40, b=20),  # Ajuste les marges internes
        height=None,  # Supprime les dimensions explicites pour permettre au CSS de contrôler la hauteur
        width=None    # Supprime les dimensions explicites pour permettre au CSS de contrôler la largeur
)
    
    cr_plots_charts = { 
                       "exited": plot(cr_plot_exited, output_type="div", include_plotlyjs=False),
                       "heatmap": plot(cr_plot_heatmap, output_type="div", include_plotlyjs=False),
                       "featureimportance": plot(cr_plot_fi, output_type="div", include_plotlyjs=False)
                       }


    return render(
        request,
        "bankchurn.html",
        {   
            "table": cr_data_describe_html,
            "cr_plots": cr_plots,
            "cr_plots_charts": cr_plots_charts,
            "cr_plots_continuous": cr_plots_continuous
            
        },
    )
       
def process_input(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        es = data.get('esValue', 50000)  # Default : 50000
        bal = data.get('balValue', 50000)
        cs = data.get('csValue', 200)
        age = data.get('ageValue', 50)
        ten = data.get('tenValue', 5)
        nb = data.get('nbValue', 3)
        
        cc = data.get('ccValue', 1)  # Default : 1 (Yes)
        am = data.get('amValue', 1)
        geo = data.get('geoValue', "France")
        gen = data.get('genValue', "Male")

        name_ten = f'Tenure_{ten}'
        name_geo = f'Geography_{geo}'
        name_am = f'IsActiveMember_{round(float(am), 2)}'
        name_nb = f'NumOfProducts_{nb}'
        name_cc = f'HasCrCard_{round(float(cc), 2)}'
        name_gen = f'Gender_{gen}'
        
        input = {'parameter' : ['EstimatedSalary', 'Balance', 'CreditScore', 'Age', 
                                name_ten, name_nb, name_cc, name_am, name_geo, name_gen], 
                 'values' : [es, bal, cs, age, 1, 1, 1, 1, 1, 1]}
        
        input_df = pd.DataFrame.from_dict(input)
        
        label = pd.DataFrame({'parameter': model.get_booster().get_score(importance_type="weight").keys()})
        X = label.merge(input_df, how='left', on='parameter').fillna(0)
        X = X.set_index('parameter').T.astype(float)
        print(f"X : {X}")
        
        proba_churn = round(model.predict_proba(X)[:, 1][0] * 100, 2)
        
        # Traitement des données
        print(f"proba churn : {proba_churn}")

        return JsonResponse({'proba_churn': proba_churn})  # Retourne du JSON
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)       
       
        
def dashboard_view(request):
    # Données des métriques
    metrics = {
        "total_visitors": 198311,
        "total_revenue": "476 874 €",
        "conversion_rate": "0.04%",
        "average_order_value": "6 036€",
        "bounce_rate": "62%",
    }

    # Données pour les graphiques
    revenue_by_price_category = {"<1000€": 5103, "<5000€": 111614, "<10000€": 92817, ">20000€": 267340}
    new_vs_returning = {"New Clients": 84.17, "Returning Clients": 15.83}
    revenue_by_client_type = {"New Clients": 106592, "Returning Clients": 370282}
    
    # colorscale
    palette = px.colors.sequential.Blues_r
    palette_map = px.colors.sequential.Blues

    # Donut Chart: Breakdown of orders by price category
    breakdown_fig = px.pie(
        names=list(revenue_by_price_category.keys()),
        values=list(revenue_by_price_category.values()),
        title="Orders by Price Category",
        color_discrete_sequence=palette
    )
    breakdown_fig.update_layout(
    autosize=True,
    margin=dict(l=20, r=20, t=30, b=20),
    paper_bgcolor="rgba(0, 0, 0, 0)",
    plot_bgcolor="rgba(0, 0, 0, 0)", 
    title_font=dict(size=14)
)  # Réduction des marges pour éviter le débordement

    # Bar Chart: Revenue by Price Category
    revenue_price_fig = px.bar(
        x=list(revenue_by_price_category.keys()),
        y=list(revenue_by_price_category.values()),
        title="Revenue by Price Category",
        text=list(revenue_by_price_category.values()),
        labels={"x": "Price Category", "y": "Revenue (€)"},
        color_discrete_sequence=palette
    )
    revenue_price_fig.update_layout(
    autosize=True,
    margin=dict(l=20, r=20, t=30, b=20),
    paper_bgcolor="rgba(0, 0, 0, 0)",
    plot_bgcolor="rgba(0, 0, 0, 0)", 
    title_font=dict(size=14),
    xaxis_title=None
)  # Réduction des marges pour éviter le débordement

    # Pie Chart: New vs Returning Clients
    client_type_fig = px.pie(
        names=list(new_vs_returning.keys()),
        values=list(new_vs_returning.values()),
        title="New vs Returning Clients",
        color_discrete_sequence=palette
    )
    client_type_fig.update_layout(
    autosize=True,
    margin=dict(l=20, r=20, t=30, b=20),
    paper_bgcolor="rgba(0, 0, 0, 0)",
    plot_bgcolor="rgba(0, 0, 0, 0)", 
    title_font=dict(size=14)
)  # Réduction des marges pour éviter le débordement

    # Bar Chart: Revenue by Client Type
    revenue_client_fig = px.bar(
        x=list(revenue_by_client_type.keys()),
        y=list(revenue_by_client_type.values()),
        title="Revenue by Client Type",
        text=list(revenue_by_client_type.values()),
        labels={"x": "Client Type", "y": "Revenue (€)"},
        color_discrete_sequence=palette
    )
    revenue_client_fig.update_layout(
    autosize=True,
    margin=dict(l=20, r=20, t=30, b=20),
    paper_bgcolor="rgba(0, 0, 0, 0)",
    plot_bgcolor="rgba(0, 0, 0, 0)", 
    title_font=dict(size=14),
    xaxis_title=None
)  # Réduction des marges pour éviter le débordement

    # Line Chart: Revenue over Time
    time_series_fig = px.line(
        x=time_series["dates"],
        y=time_series["revenue"],
        title="Revenue Over Time",
        labels={"x": "Date", "y": "Revenue (€)"},
        color_discrete_sequence=palette
    )
    time_series_fig.update_layout(
    autosize=True,
    margin=dict(l=20, r=20, t=30, b=20),
    paper_bgcolor="rgba(0, 0, 0, 0)",
    plot_bgcolor="rgba(0, 0, 0, 0)", 
    title_font=dict(size=14),
    xaxis_title=None
)  # Réduction des marges pour éviter le débordement

    map_fig = go.Figure(go.Choroplethmapbox(
        geojson=geojson_data,
        locations=df['ISO3'],
        z=df['revenue'],
        colorscale=palette_map,
        marker_line_width=0.5,
        marker_opacity=0.8,
        colorbar=dict(title="Revenue (€)")
    ))

    map_fig.update_layout(
        autosize=True,
        mapbox_style="carto-positron",   # Style de la carte
        mapbox_zoom=2.5,                  # Zoom initial
        mapbox_center={"lat": 50, "lon": 10},  # Centre de la carte
        title=dict(
            text="Revenue by country",  # Titre
            font=dict(size=14),                # Taille du titre
        ),
        coloraxis_colorbar=dict(
            title="Revenue (€)",               # Titre de la légende
            titlefont=dict(size=10),           # Taille du titre de la légende
            tickfont=dict(size=8),             # Taille des étiquettes
        ),
        margin={"r": 10, "t": 30, "l": 10, "b": 10},  # Marges réduites
        height=450,  # Hauteur totale de la figure
        width=700   # Largeur totale de la figure
)

    # Convert plots to HTML
    plots = {
        "breakdown_chart": breakdown_fig.to_html(full_html=False),
        "revenue_price_chart": revenue_price_fig.to_html(full_html=False),
        "client_type_chart": client_type_fig.to_html(full_html=False),
        "revenue_client_chart": revenue_client_fig.to_html(full_html=False),
        "time_series_chart": plot(time_series_fig, output_type="div", include_plotlyjs=False),
        "map_chart": map_fig.to_html(full_html=False),
    }

    # Pass data to the template
    return render(
        request,
        "dashboard.html",
        {
            "plots": plots,
            "metrics": metrics,
            "table": df.to_dict(orient="records"),
        },
    )
from dash_bootstrap_components._components.DropdownMenu import DropdownMenu
from dash_bootstrap_components._components.DropdownMenuItem import DropdownMenuItem
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pandas.io.formats import style
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pathlib
import pickle
# import our app
from app import app

#import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
confusion_matrix, f1_score, roc_auc_score, make_scorer)
from sklearn.model_selection import GridSearchCV 
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

#import our data
prediction_model = pickle.load(open('gradient_boost_classifier.pkl', 'rb'))

#import df to get the options
df = pd.read_csv('allegations_precinct_address_included.csv')


#dropdown options
case_year_receive = df['year_received'].unique()
case_year_close = df['year_closed'].unique()
different_fado_types = df['fado_type'].unique()
allegation_information = df['allegation'].unique()
precinct_id = df['precinct'].unique()
officer_gender = df['mos_gender'].unique()


layout = html.Div([
    # html.Label('Choose a the year of case received: '),
    # dcc.Dropdown(
    #     id='case_year_receive',
    #     options = [{'label': a, 'value' : a} for a in case_year_receive],
    #     multi = False
    # ),

    # html.Label('Choose a the year of case closed: '),
    # dcc.Dropdown(
    #     id='case_year_close',
    #     options = [{'label': b, 'value' : b} for b in case_year_close],
    #     multi = False
    # ),

    # html.Label('Choose a fado type: '),
    # dcc.Dropdown(
    #     id='different_fado_types',
    #     options = [{'label': c, 'value' : c} for c in different_fado_types],
    #     multi = False
    # ),

    # html.Label('Choose the allegation information: '),
    # dcc.Dropdown(
    #     id='allegation_information',
    #     options = [{'label': d, 'value' : d} for d in allegation_information],
    #     multi = False
    # ),

    # html.Label('Choose a precinct location id: '),
    # dcc.Dropdown(
    #     id='precinct_id',
    #     options = [{'label': e, 'value' : e} for e in precinct_id],
    #     multi = False
    # ),

    # html.Label('Choose the officer\'s gender: '),
    # dcc.Dropdown(
    #     id='officer_gender',
    #     options = [{'label': f, 'value' : f} for f in officer_gender],
    #     multi = False
    # ),
    #---------------
    html.Label(["Choose a the year of case received:",
    dcc.Dropdown(
        id='case_year_receive',
        options = [{'label': a, 'value' : a} for a in case_year_receive],
        multi = False
    )]),

    html.Label(["Choose a the year of case closed: ",
    dcc.Dropdown(
        id='case_year_close',
        options = [{'label': b, 'value' : b} for b in case_year_close],
        multi = False
    )]),

    html.Label(["Choose a fado type: ",
     dcc.Dropdown(
        id='different_fado_types',
        options = [{'label': c, 'value' : c} for c in different_fado_types],
        multi = False
    )]),

    html.Label(["Choose the allegation information: ",
     dcc.Dropdown(
        id='allegation_information',
        options = [{'label': d, 'value' : d} for d in allegation_information],
        multi = False
    )]),

    html.Label(["Choose a precinct location id: ",
     dcc.Dropdown(
        id='precinct_id',
        options = [{'label': e, 'value' : e} for e in precinct_id],
        multi = False
    )]),

    html.Label(["Choose the officer\'s gender: ",
     dcc.Dropdown(
        id='officer_gender',
        options = [{'label': f, 'value' : f} for f in officer_gender],
        multi = False
    )]),


    # html.Label(["Choose a complaint's age ", dcc.Dropdown(id='complaints_ages',
    # options = [{'label': i, 'value' : i} for i in complaints_age],
    # multi = False)]),
    # html.H1("Prediction based on NYPD Classifier Model", style={'text-align':'center'}),
    # html.Div(["Complaints Id: ", dcc.Input(id='complaints_ids', type='number')]),
    # html.Br(),
    # html.Div(["Mos Id: ", dcc.Input(id='unique_mosid', type='number')]),
    # html.Br(),
    # html.Div(["Allegation Information: ", dcc.Input(id='allegation_infos', type='number')]),
    # html.Br(),
    # html.Div(["Precinct Id: ", dcc.Input(id='precinct_ids', type='number')]),
    # html.Br(),
    # html.Div(["Complaints Ages: ", dcc.Input(id='complaints_ages', type='number')]),
    # html.Br(),
    # html.Div(id='prediction_results'),
], )

#call back
@ app.callback(
    Output(component_id='prediction_results', component_property='children'),
    Input(component_id='case_year_receive', component_property='value'),
    Input(component_id='case_year_close', component_property='value'),
    Input(component_id='different_fado_types', component_property='value'),
    Input(component_id='allegation_information', component_property='value'),
    Input(component_id='precinct_id', component_property='value'),
    Input(component_id='officer_gender', component_property='value')
)

# def show_factors(fado_Types, year_Receive, allegation_Info, precinct_Id, complaints_Age):
#     if fado_Types is None and year_Receive is None and allegation_Info is None and precinct_Id is None and complaints_Age is None:
#         raise dash.exceptions.PreventUpdate
#     else:
#         update_prediction(fado_Types, year_Receive, allegation_Info, precinct_Id, complaints_Age)

def update_prediction(case_year_receive, case_year_close, different_fado_types, allegation_information, precinct_id, officer_gender):
    my_prediction = [[case_year_receive, case_year_close, different_fado_types, allegation_information, precinct_id, officer_gender]]
    sc = StandardScaler()
    my_pred = sc.fit_transform(my_prediction)
    pred = prediction_model.predict(my_pred)
    if pred == 0:
        return 'Predict decision of the given condition is substantiated'
    else:
        return 'Predict decision of the given condition is Unsubstantiated or Exonerated'
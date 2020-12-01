from dash_bootstrap_components._components.DropdownMenu import DropdownMenu
from dash_bootstrap_components._components.DropdownMenuItem import DropdownMenuItem
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
import dash_table
# import our app
from app import app

# access our data using a relative path
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

# Load data from data folder
df_annual_ttls = pd.read_csv(DATA_PATH.joinpath('annual_totals.csv'))
df_full = pd.read_csv(DATA_PATH.joinpath(
    'allegations_precinct_address_included.csv'))

#load for officer
df_test_officer = pd.read_csv(DATA_PATH.joinpath('my_test_file.csv'))
PAGE_SIZE = 14

# Drop 2020 because data is incomplete
df_full = df_full[df_full.year_received < 2020]

# Set mapbox key
# Access mapbox api using mapbox access token
with open("./mapbox_token", 'r') as f:
    mapbox_key = f.read().strip()

#map section
map_precinct = [
    dbc.CardHeader(html.H5("Numbers of complaints over the year")),
    dbc.CardBody(
        [
           dcc.Loading(
                id="loading-bigrams-comps",
                children=[
                    dbc.Alert(
                        "Something's gone wrong! Give us a moment, but try loading this page again if problem persists.",
                        id="no-data-alert-bigrams_comp",
                        color="warning",
                        style={"display": "none"},
                    ),

                    dbc.Row(
                        [
                            dbc.Col(html.P("Choose the type of complaints:"), md=12),
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id='map_data_category',
                                        options=[
                                            {'label': 'All Complaints', 'value': 'all'},
                                            {'label': 'Abuse of Authority Complaints',
                                                'value': 'Abuse of Authority'},
                                            {'label': 'Discourtesy Complaints', 'value': 'Discourtesy'},
                                            {'label': 'Use of Force Complaints', 'value': 'Force'},
                                            {'label': 'Offensive Language Complaints',
                                                'value': 'Offensive Language'}
                                        ],
                                        value='all',
                                    ),
                                ], md = 12,
                            ),
                        ]
                    ),

                    #graph
                    dcc.Graph(id='animated_annual_map'),
                ], type="default",
            )

        ],
        style={"marginTop": 0, "marginBottom": 0, "fontSize": 15, "font-weight": "lighter"},
    ),
]

#bar chart left filter section
left_filter = dbc.Jumbotron(
    [
        html.H4("Select the filter to modifies the graph"),
        html.Hr(),
        html.Label("Choose the year to filter"),
        dcc.Dropdown(
            id='bar_graph_selector',
            options=[
                {'label': 'Year Totals', 'value': 'totals'},
                {'label': 'Complainant and Officer Genders',
                'value': 'genders'},
                {'label': 'Complainant and Officer Ethnicities',
                    'value': 'ethnicities'}
            ],
            value='totals',
            style={"marginBottom": 50, "font-size": 12}
        ),
        html.Hr(),
        html.Label("Choose the year to filter"),
        dbc.FormGroup(
            [
                dbc.Label("Year"),
                dbc.Input(id="year-input", type='number',
                        value=1989, list=list(range(1989, 2020))),
                dbc.FormText(
                    "Enter the year you want data for..."),
            ],
            style={"marginBottom": 50, "font-size": 12}
        ),            
    ]
)

#bar chart
bar_chart_graph = [
    dbc.CardHeader(html.H5("Related Visualization")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-banks-hist",
                children=[
                    dbc.Alert(
                        "Not enough data to render this plot, please adjust the filters",
                        id="no-data-alert-bank",
                        color="warning",
                        style={"display": "none"},
                    ),
                    dcc.Graph(id='user_selected_bar_graph'),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

#police officer table
table_officer = [
    dbc.CardHeader(html.H5("Related Visualization")),
    dbc.CardBody(
        [
            dcc.Loading(
                id="loading-banks-hist",
                children=[
                    dbc.Alert(
                        "Not enough data to render this plot, please adjust the filters",
                        id="no-data-alert-bank",
                        color="warning",
                        style={"display": "none"},
                    ),

                    dash_table.DataTable(
                        id='table-sorting-filtering',
                        columns=[
                            {'name': i, 'id': i, 'deletable': True} for i in sorted(df_test_officer.columns)
                        ],
                        page_current= 0,
                        page_size= PAGE_SIZE,
                        page_action='custom',

                        filter_action='custom',
                        filter_query='',

                        sort_action='custom',
                        sort_mode='multi',
                        sort_by=[],
                        style_table={'overflowX': 'auto'},
                    ),
                ],
                type="default",
            )
        ],
        style={"marginTop": 0, "marginBottom": 0},
    ),
]

#layout
BODY = dbc.Container(
    [
        dbc.Row([dbc.Col(dbc.Card(map_precinct)),], style={"marginTop": 30}),
        dbc.Row(
            [
                dbc.Col(left_filter, md=4, align="center"),
                dbc.Col(dbc.Card(bar_chart_graph), md=8),
            ],
            style={"marginTop": 30},
        ),
        dbc.Row([dbc.Col(dbc.Card(table_officer)),], style={"marginTop": 30}),
    ],
    className="mt-12",
)

layout = html.Div(children=[BODY])

# layout = html.Div([
#     # Drop down menu to select options for animated map
#     dbc.Row(
#         dbc.Col(html.Div(
#             dcc.Dropdown(
#                 id='map_data_category',
#                 options=[
#                     {'label': 'All Complaints', 'value': 'all'},
#                     {'label': 'Abuse of Authority Complaints',
#                         'value': 'Abuse of Authority'},
#                     {'label': 'Discourtesy Complaints', 'value': 'Discourtesy'},
#                     {'label': 'Use of Force Complaints', 'value': 'Force'},
#                     {'label': 'Offensive Language Complaints',
#                         'value': 'Offensive Language'}
#                 ],
#                 value='all'
#             )),
#             width={'size': 8, 'offset': 2},
#         ),
#     ),
#     dbc.Row(
#         dbc.Col(html.Div(
#             dcc.Graph(id='animated_annual_map')),
#             width={'size': 8, 'offset': 2},
#         ),
#         className='jumbotron'
#     ),
#     dbc.Row([
#         dbc.Col(
#             # Graphs chosen
#             dcc.Graph(id='user_selected_bar_graph'),
#             width={'size': 5, 'offset': 1},
#         ),
#         dbc.Col([
#             dbc.Row(
#                 dbc.Col(
#                     # Bar Graph selector dropdown
                    # dcc.Dropdown(
                    #     id='bar_graph_selector',
                    #     options=[
                    #         {'label': 'Year Totals', 'value': 'totals'},
                    #         {'label': 'Complainant and Officer Genders',
                    #          'value': 'genders'},
                    #         {'label': 'Complainant and Officer Ethnicities',
                    #             'value': 'ethnicities'}
                    #     ],
                    #     value='totals'
                    # ),
#                     width={'size': 6, 'offset': 1}
#                 )

#             ),
#             dbc.Row(
#                 dbc.Col(
#                     dbc.FormGroup(
#                         [
#                             dbc.Label("Year"),
#                             dbc.Input(id="year-input", type='number',
#                                       value=1989, list=list(range(1989, 2020))),
#                             dbc.FormText(
#                                 "Enter the year you want data for..."),
#                         ]
#                     ),
#                     width={'size': 6, 'offset': 1}
#                 )

#             ),
#         ],

#         ),
#     ]
#     ),
#     # Will base multiple figures on this input slider
#     # Slider year selector
#     html.Br(),

#     #for officer table
#     dash_table.DataTable(
#         id='table-sorting-filtering',
#         columns=[
#             {'name': i, 'id': i, 'deletable': True} for i in sorted(df_test_officer.columns)
#         ],
#         page_current= 0,
#         page_size= PAGE_SIZE,
#         page_action='custom',

#         filter_action='custom',
#         filter_query='',

#         sort_action='custom',
#         sort_mode='multi',
#         sort_by=[]
#     ),

#     html.Div(id='officer_info_div', children=[
#         html.H6('Enter officer name OR Badge Number'),
#         html.Div(["Officer First Name: ",
#                   dcc.Input(id='officer_fn',
#                             value=None, type='text'),
#                   " Last Name: ",
#                   dcc.Input(id='officer_ln',
#                             value=None, type='text'),
#                   ]),
#         html.Br(),
#         html.Div(
#             id='officer_figs_container', children=[
#                 dcc.Graph(id='officer_data_table'),
#                 dcc.Graph(id='officer_data_graph')
#             ],
#         ),
#     ])
# ]
# )

# for officer
operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

@app.callback(
    Output('table-sorting-filtering', 'data'),
    Input('table-sorting-filtering', "page_current"),
    Input('table-sorting-filtering', "page_size"),
    Input('table-sorting-filtering', 'sort_by'),
    Input('table-sorting-filtering', 'filter_query'))
def update_table(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = df_test_officer
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    page = page_current
    size = page_size
    return dff.iloc[page * size: (page + 1) * size].to_dict('records')


# Callback to hide figure containers for officer info until input is given


@ app.callback(
    Output('officer_figs_container', 'style'),
    [Input('officer_fn', 'value'), Input(
        'officer_ln', 'value')]
)
def hide_container(fn, ln):
    if fn is not None and ln is not None:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


# Callback for displaying officer info
# @ app.callback(
#     Output('officer_data_table', 'figure'),
#     [Input('officer_fn', 'value'), Input(
#         'officer_ln', 'value'), Input('officer_bn', 'value')]
# )
# def update_figure(fn, ln, bn):
#     # ToDo code to render table of Officer info
#     # Callback for map by year

@ app.callback(
    Output('animated_annual_map', 'figure'),
    [Input('map_data_category', 'value')]
)
def update_figure(category):
    # Group by year, borough, precinct
    df_cat = df_full[df_full.year_received > 1986]
    if (category != 'all'):
        # If user specified complaint type filter for that type
        df_cat = df_full[df_full['fado_type'] == category]
    precinct_grp = df_cat.groupby(by=['year_received', 'borough',
                                      'precinct', 'long', 'lat', 'fado_type'],).size()
    # Get dataframe from groupby object
    precinct_grp = precinct_grp.reset_index()
    # Change name of size(count) column to #_complaints
    precinct_grp.rename(columns={0: '#_complaints'}, inplace=True)
    # Order dataframe by year
    precinct_grp.sort_values('year_received', inplace=True)

    # Create labels dictionary for hover info
    labels = {'precinct': 'Precinct',
              'year_received': 'Complaint Year',
              '#_complaints': 'No. Complaints',
              'borough': 'Borough'}
    # Create list of columns that would appear upon hovering, using the labels above
    hover_data = {'precinct': True, 'year_received': True, 'borough': True, '#_complaints': True,
                  'long': False, 'lat': False}

    # Create scatter mapbox using same dataframe
    fig = px.scatter_mapbox(precinct_grp, lat="lat", lon="long",
                            size='#_complaints',
                            labels=labels, hover_data=hover_data, opacity=0.6,
                            animation_frame='year_received', color='fado_type', zoom=8.5,)
    fig.update_layout(mapbox_style="light",
                      mapbox_accesstoken=mapbox_key)
    fig.layout.template = 'plotly'

    return fig

# Callback for complaint type numbers by year bar graph
@ app.callback(
    Output('user_selected_bar_graph', 'figure'),
    [Input('year-input', 'value'), Input('bar_graph_selector', 'value')]
)
def update_figure(selected_year, selection):
    if selection == 'totals':
        # Callback for complaint type numbers by year bar graph
        filtered_df = df_annual_ttls[df_annual_ttls.year_received == selected_year]
        # Drop unsubstantiated_or_exnrtd since it's not relevant to this graph
        filtered_df.drop(['unsubstantiated_or_exnrtd',
                          'substantiated_(any)'], axis=1, inplace=True)
        # Drop year since we don't want it in this visualization, it's assumed from input
        filtered_df.drop('year_received', axis=1, inplace=True)
        # Transpose so we don't have to work with wideform df
        filtered_df = filtered_df.T
        # Reset index
        filtered_df.reset_index(inplace=True)
        # Name our columns so we can reference them easily when creating figure
        filtered_df.columns = ['fado_type', 'total']
        # Sort the df by total
        filtered_df.sort_values('total', ascending=False, inplace=True)
        # Build the visualization, using this filtered_df
        fig = px.bar(filtered_df, x='fado_type', y='total', )
    elif selection == 'genders':
        # Callback for gender distribution for selected year
        # Get data for selected year
        filtered_df = df_full[df_full['year_received'] == selected_year]
        # Fill null values with "unknown"
        filtered_df['complainant_gender'].fillna('Unknown', inplace=True)
        filtered_df['mos_gender'].fillna('Unknown', inplace=True)
        # Collect information about complainant ethnicity in dataframe
        comp_gender = filtered_df['complainant_gender'].value_counts()
        comp_gender = pd.DataFrame(comp_gender)
        comp_gender = comp_gender.reset_index()
        comp_gender.columns = ['comp_gender', 'comp_gender_count']
        # Collect information about officer ethnicity in datafram
        mos_gender = filtered_df['mos_gender'].value_counts()
        mos_gender = pd.DataFrame(mos_gender)
        mos_gender = mos_gender.reset_index()
        mos_gender.columns = ['mos_gender', 'mos_gender_count']

        # Join the two to get a df with both officer and complainant ethnicity by year
        filtered_df = comp_gender.join(mos_gender)

        # Build figure based on selected year
        fig = go.Figure(data=[go.Bar(name="Complainant Gender",
                                     x=filtered_df['comp_gender'],
                                     y=filtered_df['comp_gender_count']),
                              go.Bar(name="Officer Gender", x=filtered_df['mos_gender'],
                                     y=filtered_df["mos_gender_count"])
                              ])
        fig.update_layout(barmode='group')
    else:
        # Callback for ethnicity distribution for selected year
        # Get data for selected year
        filtered_df = df_full[df_full['year_received'] == selected_year]
        # Fill null values with "unknown"
        filtered_df['complainant_ethnicity'].fillna('Unknown', inplace=True)
        filtered_df['mos_ethnicity'].fillna('Unknown', inplace=True)
        # Collect information about complainant ethnicity in dataframe
        comp_eth = filtered_df['complainant_ethnicity'].value_counts()
        comp_eth = pd.DataFrame(comp_eth)
        comp_eth = comp_eth.reset_index()
        comp_eth.columns = ['comp_ethnicity', 'comp_eth_count']
        # Collect information about officer ethnicity in datafram
        mos_ethnicity = filtered_df['mos_ethnicity'].value_counts()
        mos_ethnicity = pd.DataFrame(mos_ethnicity)
        mos_ethnicity = mos_ethnicity.reset_index()
        mos_ethnicity.columns = ['mos_ethnicity', 'mos_eth_count']

        # Join the two to get a df with both officer and complainant ethnicity by year
        filtered_df = comp_eth.join(mos_ethnicity)

        # Build figure based on selected year
        fig = go.Figure(data=[go.Bar(name="Complainant Ethnicity",
                                     x=filtered_df['comp_ethnicity'],
                                     y=filtered_df['comp_eth_count']),
                              go.Bar(name="Officer Ethnicity", x=filtered_df['mos_ethnicity'],
                                     y=filtered_df["mos_eth_count"])
                              ])
        fig.update_layout(barmode='group')

    return fig


# app.layout = html.Div([
#     html.H1("Annual Data Page"),

#     dcc.Dropdown(
#         id='years-dropdown',
#         options=[
#             {'label': '1985', 'value': 1985},
#             {'label': '1986', 'value': 1986},
#             {'label': '1987', 'value': 1987}
#         ],
#         value=1985,  # initial selected value
#         multi=False,
#         style={'width': '40%'}

#     ),
#     html.Div(id='output-container'), # Where the output will go
# ])

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import itertools
import collections
import pandas as pd
import plotly.graph_objs as go

# Dataset Processing
#path = 'https://raw.githubusercontent.com/nalpalhao/DV_Practival/master/datasets/'
df = pd.read_csv('df_total.csv')

#======================================================================================================================
country_options = [dict(label=str(country), value=str(country)) for country in df['region'].unique()]
sorted_country_options = sorted(country_options, key=lambda x: x["label"])

sport_options = [dict(label=str(sport), value=str(sport)) for sport in df['Sport'].unique()]
sorted_sport_options = sorted(sport_options, key=lambda x: x["label"])


medal_options = [{'label': 'Total Medals', 'value': 'Total_Medal'},
           {'label': 'Gold Medal', 'value': 'Gold'},
           {'label': 'Silver Medal', 'value': 'Silver'},
           {'label': 'Bronze Medal', 'value': 'Bronze'},
           {'label': 'Without medal', 'value': 'Sem_Medalha'},]

dropdown_country = dcc.Dropdown(
        id='country_drop',
        options=sorted_country_options,
        value=['USA'],
        multi=True
)

dropdown_sport = dcc.Dropdown(
        id='sport_drop',
        options=sorted_sport_options,
        value=['Athletics'],
        multi=True
)

slider_year = dcc.Slider(
        id='year_slider',
        min=df['Year'].min(),
        max=df['Year'].max(),
        marks={str(i): '{}'.format(str(i)) for i in (1896, 2017, 4)},
        value=1964,
        step=1,
)


checklist_medals = dcc.RadioItems(
        id='radioitems',
        options=medal_options,
        value='Gold',
        labelStyle={'display': 'inline-block', 'margin-left':'30px'},
)
#======================================================================================================================
app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1('Olympic Games History'),

    html.Div([
        html.Div([
            html.Label('Country Choice'),
            dropdown_country,

            html.Br(), html.Br(),

            html.Label('Sport Choice'),
            dropdown_sport,

        ],style={'width': '30%'}, className='box'),

         html.Div([
               html.Div([
                   html.H2('Number of Athlets'),
                   html.H2('Number of Total Medals'),
                   html.H2('Number of Gold Medals'),
                   html.H2('Number of Silver Medal'),
                   html.H2('Number of Bronze Medal'),
                   html.H2('Number of No Medals'),
               ],style={'textAlign': 'center',  'display': 'inline'}),

               html.Br(), html.Br(), html.Br(), html.Br(),

               html.Div([
                   html.Label(id='n_athlets', className='box3', style={'left': '-26px'},),
                   html.Label(id='n_total_medal',className='box3', style={'left': '-40px'}),
                   html.Label(id='n_gold_medal',className='box3', style={'left': '-30px'} ),
                   html.Label(id='n_silver_medal', className='box3',style={'left': '-15px'}),
                   html.Label(id='n_bronze_medal', className='box3',style={'left': '-5px'}),
                   html.Label(id='n_without_medal', className='box3',style={'left': '-2px'}),
               ],style={'textAlign': 'center', 'display': 'inlinde'}),

               html.Br(), html.Br(),

               html.Div([
                   slider_year,
                   html.Div(id='slider-output-container')
               ]),
             
        ],style={'width': '70%', 'justify-content': 'center'}, className='box'),

    ], className='row'),

    html.Br(), html.Hr(), html.Br(),

    html.Div([
        html.Div([
             html.H2('Olympic City: '),
             html.Label(id='games_city', className='box'),
        ],style = {'justify-content': 'center'},className='row'),
    ], className='box'),

    html.Div([
        html.Div([
            html.H4('Medals'),
            html.Br(),

            checklist_medals,

            dcc.Graph(id='bar_graph' ),
        ], className='box',style={'width': '50%','textAlign': 'center'}),

        html.Div([

            dcc.Graph(id='bar_graph1')
            
        ], className='box',style={'width': '50%'}),

    ], style = {'justify-content': 'center'} ,className='row',),

    html.Br(),  html.Br(),
    html.H1('WORLD DATA'),

    html.Div([
        html.Div([

            dcc.Graph(id='graph3'),

        ], className='box', style={'width': '50%', 'textAlign': 'center'}),

        html.Div([

            dcc.Graph(id='graph4')

        ], className='box', style={'width': '50%'}),

    ], style={'justify-content': 'center'}, className='row', ),

    html.Br(),  html.Br(),

    html.Div([
        html.Div([

            dcc.Graph(id='graph5'),
        ], className='box'),

    ], style={'justify-content': 'center'}, className='row', ),


    html.Br(),  html.Br(),  html.Br(),

    html.Div([
            dcc.Markdown('''
            #### Dash and Markdown
            
            Dash supports [Markdown](http://commonmark.org/help).
            
            Markdown is a simple way to write and format text.
            It includes a syntax for things like **bold text** and *italics*,
            [links](http://commonmark.org/help), inline `code` snippets, lists,
            quotes, and more.
            ''', ),
    ], style = {'justify-content': 'center', }, className='box1',)
])

#======================================================================================================================

@app.callback(
    [Output("bar_graph", "figure"),
    Output("bar_graph1", "figure")],

    [Input('country_drop', 'value'),
    Input('sport_drop', 'value'),
    Input('year_slider', 'value'),
    Input('radioitems', 'value')]
)
#===================================================================================================================

def plots(countries, sport,  year, medal):

#=================================================First Bar Plot=====================================================
    df_loc = df.loc[(df['region'].isin(countries)) & (df['Sport'].isin(sport)) & (df['Year']==year)]
    df_loc1 = df_loc.groupby(by=['Interval_Age','Sex'])[medal].sum().reset_index()

    trace1 = go.Bar(
        x = list(df_loc1[df_loc1.Sex=='F']['Interval_Age']),
        y = list(df_loc1[df_loc1.Sex=='F'][medal]),
        name = 'Female',
        marker_color='pink'
    )

    trace2 = go.Bar(
        x = list(df_loc1[df_loc1.Sex=='M']['Interval_Age']),
        y = list(df_loc1[df_loc1.Sex=='M'][medal]),
        name = 'Male',
        marker_color='lightblue'
    )

    data = [trace1, trace2]

    layout_bar = dict(title=dict(text='Number of Medals per Age and Sex'),
                          yaxis=dict(title='Number of Medals'),
                          xaxis=dict(title='Age'),
                          paper_bgcolor='#f9f9f9', barmode = 'group',
                     )



#=================================================Second Bar Plot=====================================================
    df_loc = df.loc[(df['Year']==year)]

    list_country = []

    list1 = []
    list2 = []
    list3 = []

    for country in countries:
        df_bar = df_loc.loc[(df_loc['region'] == country) & (df['Sport'].isin(sport))]

        list_country.append(country)

        list1.append(df_bar['Gold'].sum())
        list2.append(df_bar['Silver'].sum())
        list3.append(df_bar['Bronze'].sum())

        trace1 = go.Bar(
            x = list1,
            y = list_country,
            name = 'Gold Medal',
            orientation='h',
            marker_color='#ffd700'
        )

        trace2 = go.Bar(
            x = list2,
            y = list_country,
            name = 'Silver Medal',
            orientation='h',
            marker_color='#c0c0c0'
        )

        trace3 = go.Bar(
            x = list3,
            y = list_country,
            name = 'Bronze Medal',
            orientation='h',
            marker_color='#cd7f32'
        )

        data1 = [trace1, trace2,trace3]

        layout_bar1 = dict(title=dict(text='Medals per Country'),
                              yaxis=dict(title='Countries'),
                              xaxis=dict(title='Number of Medals'),
                              paper_bgcolor='#f9f9f9', barmode = 'stack'
                         )

    if len(data1)==0:
        data1 = []

    return go.Figure(data=data, layout=layout_bar),\
           go.Figure(data=data1, layout=layout_bar1),


#===================================================================================================================
@app.callback(
    [
        Output('n_athlets', 'children'),
        Output('n_total_medal', 'children'),
        Output('n_gold_medal', 'children'),
        Output('n_silver_medal', 'children'),
        Output('n_bronze_medal', 'children'),
        Output('n_without_medal', 'children'),
        Output('games_city', 'children')
    ],
    [
        Input("country_drop", "value"),
        Input("year_slider", "value"),
        Input("sport_drop", "value"),
    ]
)

def indicator(countries, year, sport):
    df_loc = df.loc[(df['region'].isin(countries)) & (df['Sport'].isin(sport))].groupby(['Year']).sum().reset_index()

    if(len(df_loc.loc[df_loc['Year'] == year]['Number_Person'].values)==0):
        value_1 = 0
    else:
        value_1 = df_loc.loc[df_loc['Year'] == year]['Number_Person'].values[0]


    if (len(df_loc.loc[df_loc['Year'] == year]['Total_Medal'].values) == 0):
        value_2 = 0
    else:
        value_2 = df_loc.loc[df_loc['Year'] == year]['Total_Medal'].values[0]


    if (len(df_loc.loc[df_loc['Year'] == year]['Gold'].values) == 0):
        value_3 = 0
    else:
        value_3 = df_loc.loc[df_loc['Year'] == year]['Gold'].values[0]


    if (len(df_loc.loc[df_loc['Year'] == year]['Gold'].values) == 0):
        value_4 = 0
    else:
        value_4 = df_loc.loc[df_loc['Year'] == year]['Silver'].values[0]


    if (len(df_loc.loc[df_loc['Year'] == year]['Bronze'].values) == 0):
        value_5 = 0
    else:
        value_5 = df_loc.loc[df_loc['Year'] == year]['Bronze'].values[0]


    if (len(df_loc.loc[df_loc['Year'] == year]['Sem_Medalha'].values) == 0):
        value_6 = 0
    else:
        value_6 = df_loc.loc[df_loc['Year'] == year]['Sem_Medalha'].values[0]


    if (len(df[(df['Year']==year)]['City'].unique()) == 0):
        value_7 = 'Year without Olympic Games'
    else:
        value_7 = df[(df['Year']==year)]['City'].unique()[0]


    return str('') + str(value_1), \
           str('') + str(value_2), \
           str('') + str(value_3), \
           str('') + str(value_4), \
           str('') + str(value_5), \
           str('') + str(value_6), \
           str('') + str(value_7)


#===================================================================================================================

@app.callback(
    [Output("graph3", "figure"),
    Output("graph4", "figure")],

    [Input('year_slider', 'value'),]
)

#===================================================================================================================

def plots1(year):
#=================================================First Scatter Plot=====================================================
    df_loc = df.loc[df['Year']==year]

    dic = {}
    sorted_dict = {}

    if df_loc.empty:
        data = {'ID': [0], 'Name': ['0'], 'Sex': ['0'], 'Age': [0], 'Team': ['0'], 'NOC': ['0'], 'Games': ['0'],
            'Year': [0],
            'Season': ['0'], 'City': ['0'], 'Sport': ['0'], 'Event': ['0'], 'Medal': [0], 'Height': [0], 'Weight': [0],
            'region': ['0'], 'Number_Person': [0], 'Sem_Medalha': [0], 'Gold': [0], 'Silver': [0], 'Bronze': [0],
            'Total_Medal': [0], 'Interval_Age': ['0']}
        df_loc = pd.DataFrame.from_dict(data)

    for country in df_loc.region.unique():
        df1 = df_loc.loc[df_loc.region == country]['Total_Medal'].sum()

        dic[country]=df1

    sorted_keys = sorted(dic, key=dic.get,reverse=True)

    for w in sorted_keys:
        sorted_dict[w] = dic[w]

    sorted_dict = dict(itertools.islice(sorted_dict.items(), 10))

    trace_1 = go.Scatter(
        x=list(sorted_dict.values()),
        y=list(sorted_dict.keys()),
        mode = 'markers',
        marker=dict(
            color='black',
            symbol='star',
            size=16
        )
    )

    layout_scatter= dict(title=dict(text='Countries with more Medals'),
                              yaxis=dict(title='Countries',autorange="reversed"),
                              paper_bgcolor='#f9f9f9',

                              xaxis=dict(
                                    title='Total of Medals',
                                    showgrid=False,
                                    showline=True,
                                    linecolor='rgb(102, 102, 102)',
                                    tickfont_color='rgb(102, 102, 102)',
                                    showticklabels=True,
                                    dtick=10,
                                    ticks='outside',
                                    tickcolor='rgb(102, 102, 102)',
                            ),
    )

    data_scatter = [trace_1]

#=================================================Second Scatter Plot=====================================================
    df_loc = df.loc[df['Year']==year]

    dic = {}
    sorted_dict = {}

    if df_loc.empty:
        data = {'ID': [0], 'Name': ['0'], 'Sex': ['0'], 'Age': [0], 'Team': ['0'], 'NOC': ['0'], 'Games': ['0'],
            'Year': [0],
            'Season': ['0'], 'City': ['0'], 'Sport': ['0'], 'Event': ['0'], 'Medal': [0], 'Height': [0], 'Weight': [0],
            'region': ['0'], 'Number_Person': [0], 'Sem_Medalha': [0], 'Gold': [0], 'Silver': [0], 'Bronze': [0],
            'Total_Medal': [0], 'Interval_Age': ['0']}
        df_loc = pd.DataFrame.from_dict(data)

    for sport in df_loc.Sport.unique():
        df1 = df_loc.loc[df_loc.Sport == sport]['Number_Person'].sum()

        dic[sport]=df1

    sorted_keys = sorted(dic, key=dic.get,reverse=True)

    for w in sorted_keys:
        sorted_dict[w] = dic[w]

    sorted_dict = dict(itertools.islice(sorted_dict.items(), 10))

    trace_2 = go.Scatter(
        x=list(sorted_dict.values()),
        y=list(sorted_dict.keys()),
        mode = 'markers',
        marker=dict(
            color='black',
            symbol='star',
            size=16
        )
    )

    layout_scatter_1= dict(title=dict(text='Sports with more People'),
                              yaxis=dict(title='Sports',autorange="reversed"),
                              paper_bgcolor='#f9f9f9',

                              xaxis=dict(
                                    title ='Total of People',
                                    showgrid=False,
                                    showline=True,
                                    linecolor='rgb(102, 102, 102)',
                                    tickfont_color='rgb(102, 102, 102)',
                                    showticklabels=True,
                                    dtick=100,
                                    ticks='outside',
                                    tickcolor='rgb(102, 102, 102)',

                            ),
    )

    data_scatter_1 = [trace_2]

    return go.Figure(data=data_scatter, layout = layout_scatter), \
           go.Figure(data=data_scatter_1, layout = layout_scatter_1)

#===================================================================================================================

@app.callback(
    [Output("graph5", "figure")],

    [
    Input('year_slider', 'value'),
    ])

def plots1(year):
#=================================================First Bar Plot=====================================================
    df_loc = df.loc[(df.Year==year)]
    df_loc = df_loc.groupby(['Sport','Season'])['Number_Person'].sum().reset_index()

    if df_loc.empty:
        data = {'Sport': ['0'], 'Season': ['0'], 'Number_Person': ['0']}
        df_loc = pd.DataFrame.from_dict(data)

    df_loc_winter_sport = df_loc[df_loc.Season == 'Winter']['Sport']
    df_loc_summer_sport = df_loc[df_loc.Season == 'Summer']['Sport']

    df_loc_number_person = df_loc['Number_Person'].to_list()

    trace1 = go.Scatter(
            x = df_loc_summer_sport,
            y = df_loc_number_person,
            name = 'Summer',
            mode = 'markers',
            marker_color='#ffd700'
        )

    trace2 = go.Scatter(
            x = df_loc_winter_sport,
            y = df_loc_number_person,
            name = 'Winter',
            mode = 'markers',
            marker_color='#808080'
        )

    layout_scatter= dict(title=dict(text='Number of People per Sport'),
                              yaxis=dict(title='Number of People',
                                        dtick = 200,
                                        ),
                              paper_bgcolor='#f9f9f9',

                              xaxis=dict(
                                    title='Sports',
                                    showgrid=False,
                                    linecolor='rgb(102, 102, 102)',
                                    tickfont_color='rgb(102, 102, 102)',
                                    showticklabels=True,
                                    ticks='outside',
                                    tickcolor='rgb(102, 102, 102)',

                            ),
    )

    data = [trace1, trace2]

    return go.Figure(data = data, layout=layout_scatter),
#=====================================================================================================================
@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('year_slider', 'value')])
def update_output(value):
    return 'Year Selected: {}'.format(value)

#=====================================================================================================================

if __name__ == '__main__':
    app.run_server(debug=True)



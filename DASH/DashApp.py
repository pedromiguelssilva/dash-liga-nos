import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import base64
from os.path import join

import pandas as pd



# I. DATA GATHERING AND PREPROCESSING -----------------------------------------------------------------------------------------------------

root_path = 'assets'

FirstSeason_Order = 15

# Uploading needed dataframes
df_list_csvs = ['df_class.csv', 'df_bcr.csv', 'df_games.csv', 'df_scorers.csv', 'df_assists.csv', 'df_player_cards.csv']
df_list = []

for i in range(len(df_list_csvs)):
    df = pd.read_csv(join(root_path,
                          df_list_csvs[i]),
                     index_col = 0)

    df['Season'] = df['Season'].map(lambda x: '0' * (4 - len(str(x))) + str(x))
    df['Season'] = df['Season'].astype(str)
    df['SeasonExtended'] = df['Season'].map(lambda x: '20' + x[:2] + "/" + x[2:])
    
    df = df[df['SeasonOrder'] >= FirstSeason_Order]
    
    df_list.append(df)
    
# For readability, each dataframe will be assigned a proper name
df_class = df_list[0]                # Upload classification table (for all seasons)
df_bcr = df_list[1]                  # Upload cumulative classifications for each round (for all seasons)
df_games = df_list[2]                # Upload games (for all seasons)
df_scorers = df_list[3]              # Upload best scorers (for all seasons)
df_assists = df_list[4]              # Upload best assistants (since 0405)
df_player_cards = df_list[5]         # Upload most undisciplined players (for all seasons)



logo_liganos = root_path + r'\liga-nos-png.png'
logo_liganos_enc = base64.b64encode(open(logo_liganos, 'rb').read()).decode('ascii')





# II. APP LAYOUT -------------------------------------------------------------------------------------------------------------------------

app = dash.Dash(__name__, show_undo_redo = False)

BackgroundBlue = "#253275"



app.layout = html.Div(
    [
        # HEADER
        html.Div(
            [
                html.Div(
                    [
                        html.H1(
                            children = "MYTH BUSTERS - PRE-ASSESSMENT DASHBOARD",
                            style = {'textAlign': 'left',
                                     'fontWeight': 'bold',
                                     'marginBottom': '0.5em'}),
                    ], className = "nine columns"
                ),               
                html.Div(
                    [
                        html.Img(
                            src = 'data:image/png;base64,{}'.format(logo_liganos_enc),
                            style = {'float': 'right',
                                     'height': '70%',
                                     'width': '70%',
                                     'margin-top': -25})
                    ], className = "three columns"
                )
            ], className = 'row', style = {'marginBottom': '-1.5em'}
        ),
        
        # FILTER ROW
        html.Div(
            [
                html.Div(
                    [
                        html.H6(
                            id = 'season-slider-title',
                            children = "Select a season and check how your team performed along the way",
                            style = {'textAlign': 'left', }
                        ),
                        dcc.Slider(
                            id = 'season-slider',
                            min = df_class['SeasonOrder'].min(),
                            max = df_class['SeasonOrder'].max(),
                            value = df_class['SeasonOrder'].max(),
                            marks = df_class[['SeasonExtended', 'SeasonOrder']] \
                                            .drop_duplicates() \
                                            .set_index('SeasonOrder') \
                                            .to_dict() \
                                            ['SeasonExtended'],
                            step = None,
                            included = False)

                    ], className="eight columns"
                ),
                html.Div(
                    [
                        html.H6(
                            id = 'round-slider-title',
                            children = "Round by round storyline",
                            style = {'textAlign': 'left'}),
                        dcc.Slider(
                            id = 'round-slider',
                            min = df_bcr['Round'].min(),
                            max = df_bcr['Round'].max(),
                            value = df_bcr['Round'].max() - 5,
                            marks = {str(i): str(i) for i in df_bcr['Round'].unique()},
                            step = None,
                            included = False)
                    ], className = "four columns", style = {'margin-left': 0,
                                                            'marginBottom': '0.5em',
                                                            'float': 'right'}), 
            ], className='row', style={'marginBottom': '2.5em'}
        ),
        
        # LEFT COLUMN
        html.Div(
            [
                html.H6(
                    id = 'left-title',
                    children = "Final Classification",
                    style = {'textAlign': 'right',
                             'marginTop': '0.0em',
                             'fontWeight': 'bold'}),
                # Classification Table
                html.Div(id = 'classification-table', style = {'marginBottom': '2.0em'}),
                html.Div(
                    [
                        # 1st Card - Best Attacking Team
                        html.Div(
                            [
                                html.Br(),
                                html.P("Best Attacking Team", style = {'textAlign': 'center',
                                                                       'color': BackgroundBlue}),
                                html.P("______________________", style = {'textAlign': 'center',
                                                                          'margin-top': -15,
                                                                          'color': BackgroundBlue}),
                                html.H2(
                                    id = 'card-best-attack',
                                    children = "",
                                    style = {'textAlign': 'center',
                                             'margin-top': -3,
                                             'color': BackgroundBlue}),
                                html.P(
                                    id = 'card-best-attack-2',
                                    children = "",
                                    style = {'margin-top': -20,
                                             'color': BackgroundBlue}),
                                html.Br()
                            ], className = "two columns", style = {'background-color': 'white',
                                                                   'color': BackgroundBlue,
                                                                   'margin-left': 0,
                                                                   'width': '32%',
                                                                   'textAlign': 'center'}),
                        # 2nd Card - Best Defending Team
                        html.Div(
                            [
                                html.Br(),
                                html.P("Best Defending Team", style = {'textAlign': 'center',
                                                                       'color': BackgroundBlue}),
                                html.P("______________________", style = {'textAlign': 'center',
                                                                          'margin-top': -15,
                                                                          'color': BackgroundBlue}),
                                html.H2(
                                    id = 'card-best-deffence',
                                    children = "",
                                    style = {'textAlign': 'center',
                                             'margin-top': -3,
                                             'color': BackgroundBlue}),
                                html.P(
                                    id = 'card-best-deffence-2',
                                    children = "",
                                    style = {'margin-top': -20,
                                             'color': BackgroundBlue}),
                                html.Br()
                            ], className = "two columns", style = {'background-color': 'white',
                                                                   'color': BackgroundBlue,
                                                                   'margin-left': 0,
                                                                   'width': '32%',
                                                                   'textAlign': 'center'}),
                        # 3rd Card - Most Undisciplined Team
                        html.Div(
                            [
                                html.Br(),
                                html.P("Most Undisciplined Team", style = {'textAlign': 'center',
                                                                           'color': BackgroundBlue}),
                                html.P("______________________", style = {'textAlign': 'center',
                                                                          'margin-top': -15,
                                                                          'color': BackgroundBlue}),
                                html.H2(
                                    id = 'card-most-undisciplined',
                                    children = "",
                                    style = {'textAlign': 'center',
                                             'margin-top': -3,
                                             'color': BackgroundBlue}),
                                html.P(
                                    id = 'card-most-undisciplined-2',
                                    children = "",
                                    style = {'margin-top': -20,
                                             'color': BackgroundBlue}),
                                html.Br()
                            ], className = "two columns", style = {'background-color': 'white',
                                                                   'color': BackgroundBlue,
                                                                   'margin-left': 0,
                                                                   'width': '32%',
                                                                   'textAlign': 'center'})
                    ], style = {'display': 'flex',
                                'justify-content': 'space-between'}
                )
                
            ], className="five columns", style = {'margin-left': 0},
        ),

        # MIDDLE COLUMN
        html.Div(
            [
                #Top Scorers
                html.H6(
                    children = "Top Scorers",
                    style = {'textAlign': 'right',
                             'marginTop': '0.0em',
                             'fontWeight': 'bold'}),
                html.P("_____________________________________", style = {'textAlign': 'right',
                                                                         'marginTop': -20,
                                                                         'color': 'white'}),
                html.H5(id = 'top-scorer-1', style = {'textAlign': 'right',
                                                      'fontSize': 22,
                                                      'margin-top': -10}),
                html.H6(id = 'top-scorer-2', style = {'textAlign': 'right',
                                                      'fontSize': 15}),
                html.P(id = 'top-scorer-3', style = {'textAlign': 'right',
                                                     'fontSize': 13}),
                
                #Top Assistants
                html.H6(
                    children = "Top Assists",
                    style = {'textAlign': 'right',
                             'margin-top': 30,
                             'fontWeight': 'bold'}),
                html.P("_____________________________________", style = {'textAlign': 'right',
                                                                         'margin-top': -20,
                                                                         'color': 'white'}),
                html.H5(id = 'top-assist-1', style = {'textAlign': 'right',
                                                      'fontSize': 22,
                                                      'margin-top': -10}),
                html.H6(id = 'top-assist-2', style = {'textAlign': 'right',
                                                      'fontSize': 15}),
                html.P(id = 'top-assist-3', style = {'textAlign': 'right',
                                                     'fontSize': 13}),
                
                #Top Undisciplined
                html.H6(
                    children = "Discipline",
                    style = {'textAlign': 'right',
                             'margin-top': 30,
                             'fontWeight': 'bold'}),
                html.P("_____________________________________", style = {'textAlign': 'right',
                                                                         'margin-top': -20,
                                                                         'color': 'white'}),
                html.H5(id = 'top-discipline-1', style = {'textAlign': 'right',
                                                          'fontSize': 22,
                                                          'margin-top': -10}),
                html.H6(id = 'top-discipline-2', style = {'textAlign': 'right',
                                                          'fontSize': 15}),
                html.P(id = 'top-discipline-3', style = {'textAlign': 'right',
                                                         'fontSize': 13}),
                
                # Line Chart - Position by round for the champions of that season
                html.Div(dcc.Graph(id = 'line-chart'), style = {'margin-top': 50})

            ], className="three columns", style = {'margin-left': 60,
                                                   'marginTop': '0.0em'},
        ),   
        
        # RIGHT COLUMN
        html.Div(
            [
                html.H6(
                    id = 'right-table-title',
                    children = "Match Betting Odds and Results",
                    style = {'textAlign': 'right',
                             'marginTop': '0.0em',
                             'fontWeight': 'bold'}),
                # Games Table
                html.Div(id = 'games-table', style = {'margin-top': '0.0em',
                                                      'marginBottom': '1.0em'}),
                html.H6(
                    id = 'right-chart-title',
                    children = "Live Classification",
                    style = {'textAlign': 'right',
                             'marginTop': '0.0em',
                             'fontWeight': 'bold'}),
                # Round Classification Bar Chart
                html.Div(dcc.Graph(id = 'round-classification-bar-chart')),                
            ], className="four columns", style = {'float': 'right'},
        ),
                
    ], style = {'margin-top': 50,
                'margin-right': 100,
                'margin-left': 100,
                'margin-down': 30}
)


                
# II. APP DYNAMICS -------------------------------------------------------------------------------------------------------------------------
                
@app.callback(
    [Output(component_id = 'season-slider-title', component_property = 'children'),
     Output(component_id = 'round-slider-title', component_property = 'children'),
     Output(component_id = 'round-slider', component_property = 'min'),
     Output(component_id = 'round-slider', component_property = 'max'),
     Output(component_id = 'round-slider', component_property = 'marks'),
     Output(component_id = 'left-title', component_property = 'children'),
     Output(component_id = 'classification-table', component_property = 'children'),
     Output(component_id = 'card-best-attack', component_property = 'children'),
     Output(component_id = 'card-best-attack-2', component_property = 'children'),
     Output(component_id = 'card-best-deffence', component_property = 'children'),
     Output(component_id = 'card-best-deffence-2', component_property = 'children'),
     Output(component_id = 'card-most-undisciplined', component_property = 'children'),
     Output(component_id = 'card-most-undisciplined-2', component_property = 'children'),
     Output(component_id = 'top-scorer-1', component_property = 'children'),
     Output(component_id = 'top-scorer-2', component_property = 'children'),
     Output(component_id = 'top-scorer-3', component_property = 'children'),
     Output(component_id = 'top-assist-1', component_property = 'children'),
     Output(component_id = 'top-assist-2', component_property = 'children'),
     Output(component_id = 'top-assist-3', component_property = 'children'),
     Output(component_id = 'top-discipline-1', component_property = 'children'),
     Output(component_id = 'top-discipline-2', component_property = 'children'),
     Output(component_id = 'top-discipline-3', component_property = 'children'),
     Output(component_id = 'line-chart', component_property = 'figure'),
     Output(component_id = 'right-table-title', component_property = 'children'),
     Output(component_id = 'games-table', component_property = 'children'),
     Output(component_id = 'right-chart-title', component_property = 'children'),
     Output(component_id = 'round-classification-bar-chart', component_property = 'figure')],
    [Input(component_id = 'season-slider', component_property = 'value'),
     Input(component_id = 'round-slider', component_property = 'value')]
)
def update_season_stats(selected_season, selected_round):
    
    # I. Filtering Dataframes -------------------------------------------------------------------------------------------------------
    
    # Filtering df_class for selected_season
    df_class_filtered = df_class[df_class['SeasonOrder'] == selected_season]
    season = df_class_filtered['Season'].values[0]
    df_class_filtered = df_class_filtered[['Team', 'Games', 'Won', 'Drawn', 'Lost',
                                           'Points', 'GoalsScored', 'GoalsConceded', 'GoalsDifference', 'VE', '2A', 'A']] \
                                         .reset_index() \
                                         .rename(columns = {'index': 'Position'})
    df_class_filtered['Position'] = pd.Series([i for i in range(1, len(df_class_filtered) + 1)])
    
    # Filtering df_bcr for selected_season
    df_bcr_seasonfiltered = df_bcr[df_bcr['SeasonOrder'] == selected_season] \
                                  [['Round', 'Team', 'TotalPoints']]
                            
    # Filtering df_bcr for selected_round
    df_bcr_roundfiltered = df_bcr_seasonfiltered[df_bcr_seasonfiltered['Round'] == selected_round] \
                                                [['Team', 'TotalPoints']] \
                                                .reset_index() \
                                                .rename(columns = {'TotalPoints': 'Points'}) \
                                                .sort_values(by = 'Points')
    


    # II. FILTER ROW ---------------------------------------------------------------------------------------------------------------
    string_season = "Season " + '20' + season[:2] + '/' + season[2:]
    
    # Season Slider Title
    season_slider_title = "Check how your team performed along the years - now rewinding " + string_season
    
    # Round Slider
    round_slider_title = string_season + " storyline, by the times of round " + str(selected_round)
    round_slider_min = df_bcr_seasonfiltered['Round'].min()
    round_slider_max = df_bcr_seasonfiltered['Round'].max()
    round_slider_marks = {str(i): str(i) for i in df_bcr_seasonfiltered['Round']}
    
    

    # III. LEFT COLUMN ---------------------------------------------------------------------------------------------------------- 
    string_left = string_season + ' - Final Classification'     
    
    df_class_toshow = df_class_filtered.drop(columns = ['VE', '2A', 'A'])
    
    table_final_classification = (dash_table.DataTable(
                                                columns = [{"name": i, "id": i} for i in df_class_toshow.columns],
                                                data = df_class_toshow.to_dict('records'),
                                                style_cell = {
                                                    'textAlign': 'center',
                                                    'backgroundColor': BackgroundBlue,
                                                    'border': '0px',
                                                    'fontSize': 12,
                                                    'fontFamily': 'Segoe UI Light',
                                                    'color': 'white',
                                                    'height': 8},
                                                style_header = {
                                                    'backgroundColor': BackgroundBlue,
                                                    'textAlign': 'center',
                                                    'float': 'center',
                                                    'fontFamily': 'Segoe UI Light',
                                                    'fontWeight': 'bold',
                                                    'color': 'white'}))
    
    
    # Computing Best Defence
    best_defence = df_class_filtered[df_class_filtered['GoalsConceded'] == df_class_filtered['GoalsConceded'].min()]['Team'].values[0]
    best_defence_info = str(df_class_filtered[df_class_filtered['GoalsConceded'] == df_class_filtered['GoalsConceded'].min()] \
                                             ['GoalsConceded'] \
                                             .values[0]) \
                                             + ' Goals Conceded'
    
    # Computing Best Attack
    best_attack = df_class_filtered[df_class_filtered['GoalsScored'] == df_class_filtered['GoalsScored'].max()]['Team'].values[0]
    best_attack_info = str(df_class_filtered[df_class_filtered['GoalsScored'] == df_class_filtered['GoalsScored'].max()] \
                                            ['GoalsScored'] \
                                            .values[0]) \
                                            + ' Goals Scored'
                                            
    # Computing Most Undisciplined Team
    most_undisciplined_df = df_class_filtered.sort_values(by = ['VE', '2A', 'A'], ascending = False)
    most_undisciplined_df['TotalReds'] = most_undisciplined_df['VE'] + most_undisciplined_df['2A']
    most_undisciplined = most_undisciplined_df['Team'].values[0]
    most_undisciplined_info =  str(int(most_undisciplined_df['TotalReds'].values[0])) + " Reds, " \
                               + str(int(most_undisciplined_df['A'].values[0])) + " Yellows"
    


    # IV. MIDDLE COLUMN ----------------------------------------------------------------------------------------------------------   

    # Top Scorers, Assists and Undisciplined
    df_scorers_filtered = df_scorers[df_scorers['SeasonOrder'] == selected_season].reset_index(drop = True)
    df_assists_filtered = df_assists[df_assists['SeasonOrder'] == selected_season].reset_index(drop = True)
    df_discipline_filtered = df_player_cards[df_player_cards['SeasonOrder'] == selected_season].reset_index(drop = True)
    df_discipline_filtered['TotalReds'] = df_discipline_filtered['VE'] + df_discipline_filtered['2A']
    
    
    n_top = 3
    top_scorer = []
    top_scorer_team = []
    top_scorer_goals = []
    top_scorer_string = []
    
    top_assist = []
    top_assist_team = []
    top_assist_goals = []
    top_assist_string = []

    top_discipline = []
    top_discipline_team = []
    top_discipline_yellowcards = []
    top_discipline_redcards = []
    top_discipline_string = []

    for i in range(n_top):
        top_scorer.append(df_scorers_filtered['Player'].values[i])
        top_scorer_team.append(df_scorers_filtered['Team'].values[i])
        top_scorer_goals.append(df_scorers_filtered['G'].values[i])
        
        top_scorer_string.append(str(i+1) + ". " + top_scorer[i] \
                                 + " (" + top_scorer_team[i] + ") - " \
                                 + str(top_scorer_goals[i]) + " Goals")


        top_assist.append(df_assists_filtered['Player'].values[i])
        top_assist_team.append(df_assists_filtered['Team'].values[i])
        top_assist_goals.append(df_assists_filtered['ASS'].values[i])
        
        top_assist_string.append(str(i+1) + ". " + top_assist[i] \
                                 + " (" + top_assist_team[i] + ") - " \
                                 + str(top_assist_goals[i]) + " Assists")

        
        top_discipline.append(df_discipline_filtered['Player'].values[i])
        top_discipline_team.append(df_discipline_filtered['Team'].values[i])
        top_discipline_yellowcards.append(df_discipline_filtered['A'].values[i])
        top_discipline_redcards.append(df_discipline_filtered['TotalReds'].values[i])
        
        top_discipline_string.append(str(i+1) + ". " + top_discipline[i] \
                                     + " (" + top_discipline_team[i] + ") - " \
                                     + str(top_discipline_yellowcards[i]) + " Y, " \
                                     + str(top_discipline_redcards[i]) + " R")


    # Line Chart
    team_winner = df_class_toshow[df_class_toshow['Position'] == 1]['Team'].values[0]
    
    df_bcr_line = df_bcr[df_bcr['SeasonOrder'] == selected_season] \
                        [df_bcr['Team'] == team_winner] \
                        [['Round', 'Position']]
    
    lc_annotations = [dict(
                        x = xi,
                        y = yi,
                        text = str(yi),
                        xanchor = 'auto',
                        yanchor = 'bottom',
                        showarrow = False,
                    ) for xi, yi in zip(df_bcr_line['Round'], df_bcr_line['Position'])]
    
    line_chart = {'data': [go.Scatter(
                                x = df_bcr_line['Round'],
                                y = df_bcr_line['Position'],
                                mode = "markers + lines",
                                marker = { "color" : 'white'})],
                  'layout': go.Layout(
                                title = '<b>' + team_winner + " - Road to the Top (position by round)" + '</b>',
                                annotations = lc_annotations,
                                bargap = 0.35,
                                xaxis = dict(color = 'white',
                                             dtick = 10),
                                yaxis = dict(ticks = 'outside',
                                             tickcolor = BackgroundBlue,
                                             color = 'white'),
                                font = {"family": "Segoe UI Light", "color": "white"},
                                hovermode = 'closest',
                                paper_bgcolor = BackgroundBlue,
                                plot_bgcolor = BackgroundBlue,
                                autosize = False,
                                height = 230,
                                margin = dict(r = 0, t = 30, l = 20))}



    # V. RIGHT COLUMN ------------------------------------------------------------------------------------------------------------   
                    
    # Visuals titles
    string_right_table = "Round " + str(selected_round) + " Matches - Betting Odds and Results"
    string_right_chart = "Round " + str(selected_round) + " Live Classification"
    
    
    # Games Table    
    df_games_filtered = df_games[df_games['SeasonOrder'] == selected_season] \
                                [df_games['Round'] == selected_round] \
                                [['Date', 'B365H', 'B365D', 'B365A', 'Match']] \
                                .reset_index(drop = True)    
    
    games_table = dash_table.DataTable(
                                columns = [{"name": i, "id": i} for i in df_games_filtered.columns],
                                data = df_games_filtered.to_dict('records'),
                                style_cell={'textAlign': 'center',
                                            'backgroundColor': BackgroundBlue,
                                            'border': '0px',
                                            'fontSize': 11,
                                            'fontFamily': 'Segoe UI Light',
                                            'color': 'white',
                                            'height': 8},
                                style_header={'backgroundColor': BackgroundBlue,
                                                'textAlign': 'center',
                                                'float': 'center',
                                                'fontFamily': 'Segoe UI Light',
                                                'fontWeight': 'bold',
                                                'color': 'white'})
    
    # Live Classification Bar Chart
    bc_annotations = [dict(
                        x = xi,
                        y = yi,
                        text = str(xi),
                        xanchor = 'left',
                        font = dict(family = 'Segoe UI Light', color = 'white'),
                        showarrow = False,
                    ) for xi, yi in zip(df_bcr_roundfiltered['Points'], df_bcr_roundfiltered['Team'])]
    
    bar_chart = {'data': [go.Bar(
                            x = df_bcr_roundfiltered['Points'],
                            y = df_bcr_roundfiltered['Team'],
                            orientation='h', marker = { "color" : 'white'})],
                'layout': go.Layout(
                            bargap = 0.35,
                            annotations = bc_annotations,
                            xaxis = dict(color = 'white',
                                         dtick = 7),
                            yaxis = dict(ticks = 'outside',
                                         tickcolor = BackgroundBlue,
                                         color = 'white'),
                            font = {"family": "Segoe UI Light", "color": "white"},
                            hovermode = 'closest',
                            paper_bgcolor = BackgroundBlue,
                            plot_bgcolor = BackgroundBlue,
                            autosize = False,
                            height = 430,
                            margin = dict(r = 0, t = 0, l = 80))}
    


    # VI. Variables Returned ------------------------------------------------------------------------------------------------------------   

    return season_slider_title, \
           round_slider_title, \
           round_slider_min, \
           round_slider_max, \
           round_slider_marks, \
           string_left, \
           table_final_classification, \
           best_attack, \
           best_attack_info, \
           best_defence, \
           best_defence_info, \
           most_undisciplined, \
           most_undisciplined_info, \
           top_scorer_string[0], \
           top_scorer_string[1], \
           top_scorer_string[2], \
           top_assist_string[0], \
           top_assist_string[1], \
           top_assist_string[2], \
           top_discipline_string[0], \
           top_discipline_string[1], \
           top_discipline_string[2], \
           line_chart, \
           string_right_table, \
           games_table, \
           string_right_chart, \
           bar_chart



               


if __name__ == '__main__':
    app.run_server(debug = True, dev_tools_hot_reload = False)
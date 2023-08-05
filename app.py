# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 18:49:03 2023

@author: thoma
"""

import random
import dash
from dash import ALL
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

external_stylesheets=[dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Anniversaire Mère' 
app._favicon = ("icone.ico")
server = app.server

num=[1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13,14,14,15,15,16,16]
random.shuffle(num)

# Layout of the app
app.layout = html.Div([
    html.H1(children='Bon anniversaire Mère',style = {'textAlign': 'center','marginBottom':40,'marginTop':20}),
    html.Hr(style={'width': '70%','margin':'auto','marginBottom':20,'marginTop':20}),
    html.Div([dcc.Markdown('''
        Pour découvrir ta surprise, réussis le jeu des 50 shades de Didier. 
        Il faut trouver les paires de Didier de même couleur. Si tu ne trouves pas une paire,
        les deux cartes sélectionnées se cachent immédiatement. Des fois, ça plante un peu, 
        donc il ne faut pas hésiter à cliquer plusieurs fois pour sélectionner sa carte. 
        Bonne chance !
        ''',
        style={'width': '70%','margin-left':'220px','margin-right':'15px','textAlign': 'center'},
    )]),
    html.Hr(style={'width': '70%','margin':'auto','marginBottom':20,'marginTop':20}),
    dcc.Store(id='memory'),
    dcc.Store(id='memory_found'),
    html.Div([
        html.Button('', id={'type': 'my-button', 'index': i},className='custom-button-clicked')
        for i in range(32)
    ], style={'display': 'grid', 'grid-template-columns': 'repeat(8, 4cm)', 'gap': '10px','margin-left':'75px'}),
    html.Hr(style={'width': '70%','margin':'auto','marginBottom':20,'marginTop':20}),
    html.Div(id='out',style={'textAlign': 'center'})
])
    

@app.callback(
    Output({'type': 'my-button', 'index': ALL}, 'className'),
    Output('memory', 'data'),
    Output('memory_found', 'data'),
    Output('out','children'),
    Input({'type': 'my-button', 'index':ALL}, 'n_clicks'),
    State({'type': 'my-button', 'index': ALL}, 'className'),
    State('memory', 'data'),
    State('memory_found', 'data'),
    prevent_initial_call=True
)

def update_button_class(n_clicks, current_class,memory,memory_found):
    ctx = dash.callback_context
    button_index = ctx.triggered[0]['prop_id'][9:].split(',')[0]
    if int(button_index)==memory:
        raise PreventUpdate
    if memory_found is not None:
        if num[int(button_index)] in memory_found:
            raise PreventUpdate
    if memory == None:
        if n_clicks[int(button_index)] is not None and n_clicks[int(button_index)] % 2 == 1:
            current_class[int(button_index)]='custom-button'+str(num[int(button_index)])
            memory=int(button_index)
        else:
            current_class[int(button_index)]= 'custom-button-clicked'
    else:
        if num[int(button_index)] == num[memory]:
            current_class[int(button_index)]='custom-button'+str(num[int(button_index)])
            if memory_found is not None:  
                memory_found.append(num[int(button_index)])
            else:
                memory_found=[num[int(button_index)]]
            memory = None
        else:
            memory = None
            if memory_found is not None:
                for i in range(32):
                    if num[i] in memory_found:
                        current_class[i]='custom-button'+str(num[i])
                    else:
                        current_class[i]= 'custom-button-clicked'
            else:
                for i in range(32):
                    current_class[i]= 'custom-button-clicked'
    out=' '
    if memory_found is not None:                    
        if len(memory_found)==16:
            out=dcc.Markdown('''# [Bravo ! Et musique !](https://www.youtube.com/watch?v=HjXxvooa-0g)''')
    return current_class,memory,memory_found,out

if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=True)
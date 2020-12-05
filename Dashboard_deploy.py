import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.express as px
import numpy as np
from cube_visualization import show_cube
import base64
import io
import numpy as np
import plotly.graph_objects as go


# the style arguments for the sidebar.
SIDEBAR_STYLE = {
    
    
    'padding': '20px 10px',
    'background-color': '#f8f9fa'
}


# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '5%',
    'margin-right': '5%',
    'top': 0,
    'padding': '20px 10px'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

UPLOAD_STYLE={
        'width': '100%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
    }

TEXT_BOX_STYLE={
        'width': '100%',

    }

controls = dbc.FormGroup(
    [
        dcc.Dropdown(
            id='patchSize',
            options=[{
                'label': '99 X 99',
                'value': 99
            }, {
                'label': '49 X 49',
                'value': 49
            }
            ],
            placeholder='Patch size'
        ),
        html.Br(),
        dbc.Button(
            id='submit_button',
            n_clicks=0,
            children='Train',
            color='primary',
            block=True
        ),
    ]
)

# for parameter content
sidebar = html.Div(
    [
        html.H2('Train Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls
    ],
    style=SIDEBAR_STYLE,
)
controls_test = dbc.FormGroup(
    [
    dcc.Upload(
    id='upload-data',
    children=html.Div([
        'Drag and Drop or ',
        html.A('Select Files')
    ]),
    style=UPLOAD_STYLE,
    # Allow multiple files to be uploaded
    multiple=True
    ),

        html.Br(),
        dcc.Dropdown(
            id='patchSize_test',
            options=[{
                'label': '99 X 99',
                'value': 99
            }, {
                'label': '49 X 49',
                'value': 49
            }
            ],
            placeholder='Patch size'
        ),
        html.Br(),
        dcc.Input(id="inline_input", type="number", placeholder="Select Inline Number", style=TEXT_BOX_STYLE),
        html.Br(),
        html.Br(),
        dbc.Button(
            id='test_button',
            n_clicks=0,
            children='Test',
            color='primary',
            block=True
        ),
    ]
)

# for parameter content
sidebar_test = html.Div(
    [
        html.H2('Test Parameters', style=TEXT_STYLE),
        html.Hr(),
        controls_test
    ],
    style=SIDEBAR_STYLE
)
content_first_row = dbc.Row(
    [
     dbc.Col(sidebar),
        dbc.Col(
             dcc.Loading(
                    id="loading",
                    children=[html.Div([html.Div(id='model_trained')])],
                    type="circle",
                ), md=8,
        )
    ]
)

content_second_row = dbc.Row(
    [        
        dbc.Col(
        dcc.Tabs(id="Dashboard_tab", value='tab-1', children=[
        dcc.Tab(label='Input Data', value='tab-1'),
        dcc.Tab(label='Inline Section', value='tab-2'),
        dcc.Tab(label='Predicted Label', value='tab-3'),
        ]))
    ]
)

content_third_row=dbc.Row(
    [
        dbc.Col(html.Div(
            [
                dcc.Loading(
                    id="loading-2",
                    children=[html.Div([html.Div(id='tabs-content-example')])],
                    type="circle",
                )
            ]
        ))
    ]

)
test_part=html.Div([content_second_row, content_third_row])
final_test_part=dbc.Row([dbc.Col(sidebar_test,md=4),dbc.Col(test_part,md=8)])
# for right side content
content = html.Div(
    [
        html.H2('PETAI Analysis', style=TEXT_STYLE),
        html.Hr(),
        content_first_row,
        html.Hr(style={  'borderWidth': '1px'}),
        final_test_part        
        
    ],
    style=CONTENT_STYLE
)


# app is initialized 
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = content
import subprocess
@app.callback(Output('loading', 'model_trained'),
              [Input('submit_button', 'n_clicks')],
              [State('patchSize', 'value')])
def update_train_output(n_clicks, patch_size):
    #command="python train.py --patch_size "+str(patch_size)
    #subprocess.call(command, shell=True)
    return html.Div([
                html.H5("Training Part")
        
        ])

@app.callback(Output('tabs-content-example', 'children'),
              [Input('test_button', 'n_clicks'),
              Input('upload-data', 'contents'),
              Input('Dashboard_tab', 'value')],
              [State('patchSize_test', 'value'), State('inline_input','value'),State('upload-data', 'filename')])
def update_test_output(n_clicks, contents,tab, patch_size, inline_number,filename):
        content_type, content_string = contents[0].split(',')
        decoded = base64.b64decode(content_string)
        file_like_object = io.BytesIO(decoded)
        vol = np.load(file_like_object,allow_pickle=True)
        
        volume=vol[:100,:patch_size,:patch_size]
        volume = volume.T
        
        if tab == 'tab-1':
            fig=show_cube(volume)
            return html.Div([
                dcc.Graph(figure=fig)
        
            ])
        elif tab == 'tab-2':
            fig2 = px.imshow(vol[inline_number])
            return html.Div([
                dcc.Graph(figure=fig2)
        
        ])
        elif tab == 'tab-3':
            #command="python test.py --patch_size "+str(patch_size)+"--inline_number"+str(inline_number)
            #subprocess.call(command, shell=True)

            return html.Div([
                html.H5("Tab content 3")
        
        ])   

#  main calling 
if __name__ == '__main__':
    app.run_server(debug=False)
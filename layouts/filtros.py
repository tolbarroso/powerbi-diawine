from dash import dcc, html

def filtros():
    return html.Div([
        html.Label('Equipe:'),
        dcc.Dropdown(
            id='filtro-equipe',
            options=[{'label': equipe, 'value': equipe} for equipe in ['Equipe A', 'Equipe B']],
            multi=True
        ),
        
        html.Label('RCA:'),
        dcc.Dropdown(
            id='filtro-rca',
            options=[{'label': rca, 'value': rca} for rca in ['RCA 1', 'RCA 2']],
            multi=True
        ),

        html.Label('Departamento:'),
        dcc.Dropdown(
            id='filtro-departamento',
            options=[{'label': dept, 'value': dept} for dept in ['Departamento 1', 'Departamento 2']],
            multi=True
        ),

        html.Label('Período de Comparação:'),
        dcc.DatePickerRange(
            id='filtro-periodo',
            start_date='2024-01-01',
            end_date='2024-09-30'
        )
    ], style={'padding': '10px'})

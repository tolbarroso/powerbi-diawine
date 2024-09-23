from dash import dcc, html

def filtros():
    return html.Div([
        html.Div([
            html.Label('Equipe:', className="filter-label"),
            dcc.Dropdown(
                id='filtro-equipe',
                options=[{'label': equipe, 'value': equipe} for equipe in ['Equipe A', 'Equipe B']],
                multi=True,
                className="dropdown"
            ),
        ], className="filter-item"),

        html.Div([
            html.Label('RCA:', className="filter-label"),
            dcc.Dropdown(
                id='filtro-rca',
                options=[{'label': rca, 'value': rca} for rca in ['RCA 1', 'RCA 2']],
                multi=True,
                className="dropdown"
            ),
        ], className="filter-item"),

        html.Div([
            html.Label('Departamento:', className="filter-label"),
            dcc.Dropdown(
                id='filtro-departamento',
                options=[{'label': dept, 'value': dept} for dept in ['Dept 1', 'Dept 2']],
                multi=True,
                className="dropdown"
            ),
        ], className="filter-item"),

        html.Div([
            html.Label('Período de Comparação:', className="filter-label"),
            dcc.DatePickerRange(
                id='filtro-periodo',
                start_date='2024-01-01',
                end_date='2024-09-30',
                display_format='MMM Do, YY'
            )
        ], className="filter-item"),
    ], className="filters-container")

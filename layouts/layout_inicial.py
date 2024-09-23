from dash import dcc, html
from layouts.filtros import filtros

def layout_inicial():
    return html.Div([
        html.H1("Dashboard Dia Wine", style={'textAlign': 'center', 'color': '#FFFFFF'}),
        
        # Filtros
        filtros(),

        # Gráficos principais
        html.Div([
            dcc.Graph(id='comparativo-periodo'),
            dcc.Graph(id='vendas-mes'),
            dcc.Graph(id='vendas-ano-passado'),
            dcc.Graph(id='produtos-mais-vendidos'),
            dcc.Graph(id='ticket-medio')
        ]),
        
        # Botão para exportar PDF
        html.Button('Exportar para PDF', id='exportar-pdf', n_clicks=0)
    ])

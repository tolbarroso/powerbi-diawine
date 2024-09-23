from dash import dcc, html
from layouts.filtros import filtros

def layout_inicial():
    return html.Div([
        html.H1("Dashboard Dia Wine", className="title"),
        
        # Filtros na parte superior
        filtros(),

        # Gráficos principais
        html.Div([
            dcc.Graph(id='comparativo-periodo', className="graph"),
            dcc.Graph(id='vendas-mes', className="graph"),
            dcc.Graph(id='vendas-ano-passado', className="graph"),
            dcc.Graph(id='produtos-mais-vendidos', className="graph"),
            dcc.Graph(id='ticket-medio', className="graph")
        ], className="grid"),

        # Botão para exportar PDF
        html.Div(
            html.Button('Exportar para PDF', id='exportar-pdf', n_clicks=0, className="pdf-button")
        ),
    ], className="container")

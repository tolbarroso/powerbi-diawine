import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import pdfkit

# Carregar os dados
df = pd.read_excel('planilhas/dados_dia_wine.xlsx', sheet_name=None)

# Criar a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Layout do Dashboard
app.layout = dbc.Container([
    # Cabeçalho com logo e título
    dbc.Row([
        dbc.Col(html.Img(src=app.get_asset_url('logo.png'), height="60px"), width="auto"),
        dbc.Col(html.H1("Dashboard Dia Wine", style={'color': '#F6C62D', 'textAlign': 'center'}), width=True)
    ], justify="between", align="center", className='mb-4'),

    # Filtros
    dbc.Row([
        dbc.Col([
            html.Label("Equipe", style={'color': '#FFFFFF'}),
            dcc.Dropdown(
                id='filter-equipe',
                options=[{'label': equipe, 'value': equipe} for equipe in df['Equipes']['Equipe'].unique()],
                multi=True,
                value=[]
            )
        ], width=4),
        
        dbc.Col([
            html.Label("RCA", style={'color': '#FFFFFF'}),
            dcc.Dropdown(
                id='filter-rca',
                options=[{'label': rca, 'value': rca} for rca in df['RCA']['RCA'].unique()],
                multi=True,
                value=[]
            )
        ], width=4),

        dbc.Col([
            html.Label("Departamento", style={'color': '#FFFFFF'}),
            dcc.Dropdown(
                id='filter-departamento',
                options=[{'label': dep, 'value': dep} for dep in df['Departamentos']['Departamento'].unique()],
                multi=True,
                value=[]
            )
        ], width=4)
    ], className='mb-4'),

    # Gráficos
    dbc.Row([
        dbc.Col(dcc.Graph(id='vendas-periodo'), width=6),
        dbc.Col(dcc.Graph(id='ticket-medio'), width=6)
    ], className='mb-4'),

    # Gráfico de mix de vendas e positividade
    dbc.Row([
        dbc.Col(dcc.Graph(id='mix-vendas'), width=6),
        dbc.Col(dcc.Graph(id='positivacao'), width=6)
    ], className='mb-4'),

    # Botão para exportação em PDF
    dbc.Row([
        dbc.Col(html.Button("Exportar PDF", id="btn-export-pdf", className="btn btn-warning"), width={"size": 3, "offset": 9})
    ]),

    dcc.Download(id='download-pdf')
], fluid=True, style={'backgroundColor': '#151D52'})

# Callbacks para atualizar os gráficos dinamicamente
@app.callback(
    [Output('vendas-periodo', 'figure'),
     Output('ticket-medio', 'figure'),
     Output('mix-vendas', 'figure'),
     Output('positivacao', 'figure')],
    [Input('filter-equipe', 'value'),
     Input('filter-rca', 'value'),
     Input('filter-departamento', 'value')]
)
def update_graphs(selected_equipes, selected_rcas, selected_departamentos):
    # Filtrar os dados com base nas seleções
    filtered_df = df['Vendas']
    if selected_equipes:
        filtered_df = filtered_df[filtered_df['Equipe'].isin(selected_equipes)]
    if selected_rcas:
        filtered_df = filtered_df[filtered_df['RCA'].isin(selected_rcas)]
    if selected_departamentos:
        filtered_df = filtered_df[filtered_df['Departamento'].isin(selected_departamentos)]

    # Gráficos
    vendas_fig = px.line(filtered_df, x='Período', y='Vendas', title="Vendas por Período")
    ticket_medio_fig = px.bar(filtered_df, x='Período', y='Ticket Médio', title="Ticket Médio por Período")
    mix_vendas_fig = px.pie(filtered_df, names='Produto', values='Vendas', title="Mix de Vendas")
    positivacao_fig = px.scatter(filtered_df, x='Vendas', y='Positivação', color='Vendedor', title="Positivação por Vendedor")

    return vendas_fig, ticket_medio_fig, mix_vendas_fig, positivacao_fig

# Callback para exportar o layout em PDF
@app.callback(
    Output('download-pdf', 'data'),
    [Input('btn-export-pdf', 'n_clicks')],
    prevent_initial_call=True
)
def export_pdf(n_clicks):
    pdf_file = 'report.pdf'
    pdfkit.from_file('templates/layout.html', pdf_file)
    return dcc.send_file(pdf_file)

if __name__ == '__main__':
    app.run_server(debug=True)

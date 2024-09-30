import dash
from dash import dcc, html 
import dash_bootstrap_components as dbc  
import pandas as pd  
import plotly.express as px  
from dash.dependencies import Input, Output  
import pdfkit  

# Carregar os dados da planilha Excel
df = pd.read_excel('planilhas/dados_dia_wine.xlsx', sheet_name='Vendas')
print(df.columns.tolist())  # Verifique os nomes das colunas

# Inicializando a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Configure the path to wkhtmltopdf executable
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')  # Verifique se este caminho está correto

# Layout do Dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Img(src=app.get_asset_url('logo.png'), height="60px"), width="auto"),
        dbc.Col(html.H1("Dashboard Dia Wine", style={'color': '#F6C62D', 'textAlign': 'center'}), width=True)
    ], justify="between", align="center", className='mb-4'),

    dbc.Row([
        dbc.Col([  # Filtro Código
            html.Label("Código", style={'color': '#FFFFFF'}),
            dcc.Dropdown(
                id='filter-codigo',
                options=[{'label': str(codigo), 'value': codigo} for codigo in df['Código'].unique()],
                multi=True,
                value=[]
            )
        ], width=4),
        
        dbc.Col([  # Filtro Nome
            html.Label("Nome", style={'color': '#FFFFFF'}),
            dcc.Dropdown(
                id='filter-nome',
                options=[{'label': nome, 'value': nome} for nome in df['Nome'].unique()],
                multi=True,
                value=[]
            )
        ], width=4),

        dbc.Col([  # Filtro Qt. Vendida
            html.Label("Qt. Vendida", style={'color': '#FFFFFF'}),
            dcc.Dropdown(
                id='filter-qt_vendida',
                options=[{'label': str(vendida), 'value': vendida} for vendida in df['Qt. Vendida'].unique() if pd.notna(vendida)],
                multi=True,
                value=[]
            )
        ], width=4)
    ], className='mb-4'),

    dbc.Row([
        dbc.Col(dcc.Graph(id='vendas-periodo'), width=6),
        dbc.Col(dcc.Graph(id='ticket-medio'), width=6)
    ], className='mb-4'),

    dbc.Row([
        dbc.Col(dcc.Graph(id='mix-vendas'), width=6),
        dbc.Col(dcc.Graph(id='positivacao'), width=6)
    ], className='mb-4'),

    dbc.Row([
        dbc.Col(html.Button("Exportar PDF", id="btn-export-pdf", className="btn btn-warning"), width={"size": 3, "offset": 9})
    ]),

    dcc.Download(id='download-pdf')
], fluid=True, style={'backgroundColor': '#151D52'})

@app.callback(
    [Output('vendas-periodo', 'figure'),
     Output('ticket-medio', 'figure'),
     Output('mix-vendas', 'figure'),
     Output('positivacao', 'figure')],
    [Input('filter-codigo', 'value'),
     Input('filter-nome', 'value'),
     Input('filter-qt_vendida', 'value')]
)
def update_graphs(selected_codigos, selected_nomes, selected_vendidas):
    filtered_df = df

    if selected_codigos:
        filtered_df = filtered_df[filtered_df['Código'].isin(selected_codigos)]
    if selected_nomes:
        filtered_df = filtered_df[filtered_df['Nome'].isin(selected_nomes)]
    if selected_vendidas:
        filtered_df = filtered_df[filtered_df['Qt. Vendida'].isin(selected_vendidas)]

    vendas_fig = px.line(filtered_df, x='Nome', y='Qt. Vendida', title="Vendas por Nome")
    ticket_medio_fig = px.bar(filtered_df, x='Nome', y='Vl.Vendido', title="Valor Vendido por Nome")  # Correção aqui
    mix_vendas_fig = px.pie(filtered_df, names='Nome', values='Qt. Vendida', title="Mix de Vendas")
    positivacao_fig = px.scatter(filtered_df, x='Qt. Vendida', y='% Pos.', color='Nome', title="Positivação por Vendedor")

    return vendas_fig, ticket_medio_fig, mix_vendas_fig, positivacao_fig

@app.callback(
    Output('download-pdf', 'data'),
    [Input('btn-export-pdf', 'n_clicks')],
    prevent_initial_call=True
)
def export_pdf(n_clicks):
    pdf_file = 'report.pdf'
    pdfkit.from_file('templates/layout.html', pdf_file, configuration=config)  # Verifique se o caminho para o layout.html está correto
    return dcc.send_file(pdf_file)

if __name__ == '__main__':
    app.run_server(debug=True)

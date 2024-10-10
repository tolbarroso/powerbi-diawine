import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import pdfkit

# Carregar os dados da planilha Excel
df = pd.read_excel('planilhas/dados_dia_wine.xls', sheet_name='planilha')

# Inicializando a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])  # Usando Bootstrap

# Configuração para pdfkit
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

# Layout do Dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Img(src=app.get_asset_url('logo.png'), height="60px"), width="auto"),
        dbc.Col(html.H1("Dashboard Dia Wine", style={'color': '#007BFF', 'textAlign': 'center'}), width=True)
    ], justify="between", align="center", className='mb-4'),

    # Filtros
    dbc.Row([
        dbc.Col([html.Label("CNPJ"), dcc.Input(id='filter-cgcent', type='text', placeholder='Digite o CNPJ')], width=2),
        dbc.Col([html.Label("Código do Cliente"),
                 dcc.Dropdown(id='filter-codcli',
                              options=[{'label': str(cod), 'value': cod} for cod in df['COD CLIENTE'].unique() if pd.notna(cod)],
                              multi=True)], width=2),
        dbc.Col([html.Label("Nome Fantasia"), dcc.Input(id='filter-fantasia', type='text', placeholder='Digite o Nome Fantasia')], width=2),
        dbc.Col([html.Label("Razão Social"), dcc.Input(id='filter-cliente', type='text', placeholder='Digite o Nome do Cliente')], width=2),
        dbc.Col([html.Label("Bairro"), dcc.Input(id='filter-bairro', type='text', placeholder='Digite o Bairro')], width=2),
        dbc.Col([html.Label("Município"), dcc.Input(id='filter-municipio', type='text', placeholder='Digite o Município')], width=2)
    ], className='mb-4'),
    
    dbc.Row([
        dbc.Col([html.Label("Código do Produto"),
                 dcc.Dropdown(id='filter-codprod',
                              options=[{'label': str(cod), 'value': cod} for cod in df['COD PROD'].unique() if pd.notna(cod)],
                              multi=True)], width=2),
        dbc.Col([html.Label("Produto"), dcc.Input(id='filter-produto', type='text', placeholder='Digite o Nome do Produto')], width=2),
        dbc.Col([html.Label("Embalagem"), dcc.Input(id='filter-embalagem', type='text', placeholder='Digite a Litragem')], width=2),
        dbc.Col([html.Label("Quantidade"), dcc.Input(id='filter-qt', type='number', placeholder='Quantidade Mínima')], width=2),
        dbc.Col([html.Label("Valor Total"), dcc.Input(id='filter-total', type='number', placeholder='Valor Total Mínimo')], width=2),
        dbc.Col([html.Label("RCA"),
                 dcc.Dropdown(id='filter-codusur',
                              options=[{'label': rca, 'value': rca} for rca in df['RCA'].unique() if pd.notna(rca)],
                              multi=True)], width=2)
    ], className='mb-4'),

    dbc.Row([
        dbc.Col([html.Label("Vendedor"), dcc.Input(id='filter-vendedor', type='text', placeholder='Digite o Nome do Vendedor')], width=2),
        dbc.Col([html.Label("Supervisor"), dcc.Input(id='filter-supervisor', type='text', placeholder='Digite o Nome do Supervisor')], width=2),
        dbc.Col([html.Label("Departamento"),
                 dcc.Dropdown(id='filter-depto',
                              options=[{'label': dep, 'value': dep} for dep in df['DEPARTAMENTO'].unique() if pd.notna(dep)],
                              multi=True)], width=2),
        dbc.Col([html.Label("Data de Faturamento"),
                 dcc.DatePickerRange(id='filter-dtfat', display_format="DD-MM-YYYY")], width=4),
        dbc.Col([html.Label("Ramo"), dcc.Input(id='filter-ramo', type='text', placeholder='Digite o Ramo')], width=2)
    ], className='mb-4'),

    # Gráficos
    dbc.Row([
        dbc.Col(dcc.Graph(id='vendas-grafico'), width=6),
        dbc.Col(dcc.Graph(id='clientes-grafico'), width=6)
    ], className='mb-4'),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='positivacao-grafico'), width=6),
        dbc.Col(dcc.Graph(id='meta-vendas-grafico'), width=6)
    ], className='mb-4'),
    
    dbc.Button("Exportar PDF", id="btn-export-pdf", color="primary", className='mt-4'),

    # Div para mensagem de feedback
    html.Div(id='feedback-message', style={'marginTop': '20px', 'color': 'green'})
], fluid=True, style={'backgroundColor': '#F8F9FA'})  # Fundo claro

# Callbacks para atualizar os gráficos
@app.callback(
    [Output('vendas-grafico', 'figure'),
     Output('clientes-grafico', 'figure'),
     Output('positivacao-grafico', 'figure'),
     Output('meta-vendas-grafico', 'figure')],
    [Input('filter-cgcent', 'value'), Input('filter-codcli', 'value'), Input('filter-fantasia', 'value'),
     Input('filter-cliente', 'value'), Input('filter-bairro', 'value'), Input('filter-municipio', 'value'),
     Input('filter-codprod', 'value'), Input('filter-produto', 'value'), Input('filter-embalagem', 'value'),
     Input('filter-qt', 'value'), Input('filter-total', 'value'), Input('filter-codusur', 'value'),
     Input('filter-vendedor', 'value'), Input('filter-supervisor', 'value'), Input('filter-depto', 'value'),
     Input('filter-dtfat', 'start_date'), Input('filter-dtfat', 'end_date'), Input('filter-ramo', 'value')]
)
def update_graphs(cgcent, selected_clientes, fantasia, cliente, bairro, municipio, selected_produtos, produto,
                   embalagem, qt, total, selected_rcas, vendedor, supervisor, selected_departamentos, start_date, end_date, ramo):
    # Filtrar os dados
    filtered_df = df
    if cgcent: filtered_df = filtered_df[filtered_df['CNPJ'].str.contains(cgcent, case=False)]
    if selected_clientes: filtered_df = filtered_df[filtered_df['COD CLIENTE'].isin(selected_clientes)]
    if fantasia: filtered_df = filtered_df[filtered_df['NOME FANTASIA'].str.contains(fantasia, case=False)]
    if cliente: filtered_df = filtered_df[filtered_df['RAZÃO SOCIAL'].str.contains(cliente, case=False)]
    if bairro: filtered_df = filtered_df[filtered_df['BAIRRO'].str.contains(bairro, case=False)]
    if municipio: filtered_df = filtered_df[filtered_df['MUNICIPIO'].str.contains(municipio, case=False)]
    if selected_produtos: filtered_df = filtered_df[filtered_df['COD PROD'].isin(selected_produtos)]
    if produto: filtered_df = filtered_df[filtered_df['PRODUTO'].str.contains(produto, case=False)]
    if embalagem: filtered_df = filtered_df[filtered_df['EMBALAGEM'].str.contains(embalagem, case=False)]
    if qt: filtered_df = filtered_df[filtered_df['QT'] >= qt]
    if total: filtered_df = filtered_df[filtered_df['TOTAL'] >= total]
    if selected_rcas: filtered_df = filtered_df[filtered_df['RCA'].isin(selected_rcas)]
    if vendedor: filtered_df = filtered_df[filtered_df['NOME VENDEDOR'].str.contains(vendedor, case=False)]
    if supervisor: filtered_df = filtered_df[filtered_df['NOME SUPERVISOR'].str.contains(supervisor, case=False)]
    if selected_departamentos: filtered_df = filtered_df[filtered_df['DEPARTAMENTO'].isin(selected_departamentos)]
    if start_date and end_date: filtered_df = filtered_df[(filtered_df['DT FAT'] >= start_date) & (filtered_df['DT FAT'] <= end_date)]
    if ramo: filtered_df = filtered_df[filtered_df['SEGUIMENTO'].str.contains(ramo, case=False)]

    # Gráficos
    vendas_fig = px.bar(filtered_df, x='PRODUTO', y='TOTAL', title='Total de Vendas por Produto')
    clientes_fig = px.pie(filtered_df, names='RAZÃO SOCIAL', values='TOTAL', title='Distribuição de Vendas por Cliente')
    positivacao_fig = px.line(filtered_df, x='NOME VENDEDOR', y='QT', title='Positivação por Vendedor')
    meta_vendas_fig = px.scatter(filtered_df, x='QT', y='TOTAL', title='Meta x Vendas Realizadas')

    return vendas_fig, clientes_fig, positivacao_fig, meta_vendas_fig

# Callback para exportar o PDF
@app.callback(
    Output('feedback-message', 'children'),
    Input('btn-export-pdf', 'n_clicks')
)
def export_pdf(n_clicks):
    if n_clicks:
        # Gerar o HTML a partir do layout do Dash
        html_content = app.get_asset_url('layout.html')
        pdfkit.from_string(html_content, 'dashboard_dia_wine.pdf', configuration=config)
        return "PDF gerado com sucesso!"
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)

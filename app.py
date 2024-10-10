import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.io as pio
from dash.dependencies import Input, Output
import pdfkit

# Carregar os dados da planilha Excel
df = pd.read_excel('planilhas/dados_dia_wine.xls', sheet_name='planilha')

# Inicializando a aplicação Dash com tema Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Configuração para pdfkit
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

# Layout do Dashboard com fundo preto
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Img(src=app.get_asset_url('logo.png'), height="60px"), width="auto"),
        dbc.Col(html.H1("Dashboard Dia Wine", style={'color': '#F6C62D', 'textAlign': 'center'}), width=True)
    ], justify="between", align="center", className='mb-4'),

    # Filtros simplificados
    dbc.Row([
        dbc.Col([html.Label("Cód. Cliente"), dcc.Dropdown(id='filter-codcli',
                 options=[{'label': str(cod), 'value': cod} for cod in df['COD CLIENTE'].unique()],
                 multi=True)], width=2),
        
        dbc.Col([html.Label("Cód. Produto"), dcc.Dropdown(id='filter-codprod',
                 options=[{'label': str(cod), 'value': cod} for cod in df['COD PROD'].unique()],
                 multi=True)], width=2),
        
        dbc.Col([html.Label("RCA"), dcc.Dropdown(id='filter-rca',
                 options=[{'label': rca, 'value': rca} for rca in df['RCA'].unique()],
                 multi=True)], width=2),
        
        dbc.Col([html.Label("Departamento"), dcc.Dropdown(id='filter-depto',
                 options=[{'label': dept, 'value': dept} for dept in df['DEPARTAMENTO'].unique()],
                 multi=True)], width=2),
        
        dbc.Col([html.Label("Data de Fat"), dcc.DatePickerRange(id='filter-dtfat', display_format="DD-MM-YYYY")], width=2),
        
        dbc.Col([html.Label("Seguimento"), dcc.Dropdown(id='filter-seguimento',
                 options=[{'label': seg, 'value': seg} for seg in df['SEGUIMENTO'].unique()],
                 multi=True)], width=2),
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
    
    dbc.Button("Exportar PDF", id="btn-export-pdf", color="primary", className='mt-4')
], fluid=True, style={'backgroundColor': '#000000'})  # Fundo preto

# Callbacks para atualizar os gráficos e salvar as imagens
@app.callback(
    [Output('vendas-grafico', 'figure'),
     Output('clientes-grafico', 'figure'),
     Output('positivacao-grafico', 'figure'),
     Output('meta-vendas-grafico', 'figure')],
    [Input('filter-codcli', 'value'), Input('filter-codprod', 'value'), Input('filter-rca', 'value'),
     Input('filter-depto', 'value'), Input('filter-dtfat', 'start_date'), Input('filter-dtfat', 'end_date'),
     Input('filter-seguimento', 'value')]
)
def update_graphs(selected_clientes, selected_produtos, selected_rcas, selected_departamentos, start_date, end_date, seguimento):
    # Filtrar os dados com base nos filtros aplicados
    filtered_df = df.copy()
    if selected_clientes: filtered_df = filtered_df[filtered_df['COD CLIENTE'].isin(selected_clientes)]
    if selected_produtos: filtered_df = filtered_df[filtered_df['COD PROD'].isin(selected_produtos)]
    if selected_rcas: filtered_df = filtered_df[filtered_df['RCA'].isin(selected_rcas)]
    if selected_departamentos: filtered_df = filtered_df[filtered_df['DEPARTAMENTO'].isin(selected_departamentos)]
    if start_date and end_date: filtered_df = filtered_df[(filtered_df['DT FAT'] >= start_date) & (filtered_df['DT FAT'] <= end_date)]
    if seguimento: filtered_df = filtered_df[filtered_df['SEGUIMENTO'].isin(seguimento)]
    
    # Criação de gráficos simplificados
    vendas_fig = px.bar(filtered_df, x='PRODUTO', y='TOTAL', title='Vendas por Produto', text_auto=True)
    clientes_fig = px.bar(filtered_df, x='CLIENTE', y='QT', title='Clientes por Produto', text_auto=True)
    positivacao_fig = px.line(filtered_df, x='DT FAT', y='QT', title='Positivação por Período')
    meta_vendas_fig = px.bar(filtered_df, x='DEPARTAMENTO', y='TOTAL', title='Meta x Vendas', text_auto=True)

    # Ajustes visuais para clareza
    for fig in [vendas_fig, clientes_fig, positivacao_fig, meta_vendas_fig]:
        fig.update_layout(title_font_size=16, title_font_color="#F6C62D", plot_bgcolor="#000000", paper_bgcolor="#000000")
    
    # Salvar gráficos como imagens
    pio.write_image(vendas_fig, 'templates/vendas_plot.png')
    pio.write_image(clientes_fig, 'templates/clientes_plot.png')
    pio.write_image(positivacao_fig, 'templates/positivacao_plot.png')
    pio.write_image(meta_vendas_fig, 'templates/meta_vendas_plot.png')

    return vendas_fig, clientes_fig, positivacao_fig, meta_vendas_fig

# Callback para exportar o PDF
@app.callback(
    Output('btn-export-pdf', 'n_clicks'),
    Input('btn-export-pdf', 'n_clicks'),
    prevent_initial_call=True
)
def export_pdf(n_clicks):
    options = {'page-size': 'A4', 'encoding': 'UTF-8'}
    pdfkit.from_file('templates/layout.html', 'dashboard_dia_wine.pdf', configuration=config, options=options)
    return None

# Executar a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)

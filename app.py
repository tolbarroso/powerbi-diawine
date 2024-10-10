import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.io as pio
from dash.dependencies import Input, Output
import pdfkit
import io
import flask
from flask import send_file

# Carregar os dados da planilha Excel
df = pd.read_excel('planilhas/dados_dia_wine.xls', sheet_name='planilha')

# Função para encurtar os nomes
def abreviar_nome(nome, max_length=15):
    if len(nome) > max_length:
        return nome[:max_length] + '...'
    return nome

# Aplicar a função de abreviação nos campos "PRODUTO" e "NOME FANTASIA"
df['PRODUTO ABV'] = df['PRODUTO'].apply(lambda x: abreviar_nome(x))
df['NOME FANTASIA ABV'] = df['NOME FANTASIA'].apply(lambda x: abreviar_nome(x))

# Inicializando a aplicação Dash com tema Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Necessário para as exportações

# Configuração para pdfkit
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

# Layout do Dashboard
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
    
    dbc.Button("Exportar PDF", id="btn-export-pdf", color="primary", className='mt-4'),
    dbc.Button("Exportar para Excel", id="btn-export-excel", color="secondary", className='mt-4 mx-2'),
    dbc.Button("Exportar para CSV", id="btn-export-csv", color="info", className='mt-4')
], fluid=True, style={'backgroundColor': '#000000'})  # Fundo preto

# Callbacks para atualizar os gráficos
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
    
    # Gráficos simplificados e dinâmicos com fundo branco e cores para cada produto
    vendas_fig = px.bar(filtered_df, x='PRODUTO ABV', y='TOTAL', title='Vendas por Produto', text_auto=True, color='PRODUTO ABV')
    clientes_fig = px.bar(filtered_df, x='NOME FANTASIA ABV', y='QT', title='Clientes por Produto', text_auto=True, color='NOME FANTASIA ABV')
    positivacao_fig = px.line(filtered_df, x='DT FAT', y='QT', title='Positivação por Período')
    meta_vendas_fig = px.bar(filtered_df, x='DEPARTAMENTO', y='TOTAL', title='Meta x Vendas', text_auto=True, color='DEPARTAMENTO')

    # Ajustes visuais: fundo branco
    for fig in [vendas_fig, clientes_fig, positivacao_fig, meta_vendas_fig]:
        fig.update_layout(title_font_size=16, title_font_color="#F6C62D", plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF")

    return vendas_fig, clientes_fig, positivacao_fig, meta_vendas_fig

# Função para exportar PDF
@app.callback(
    Output('btn-export-pdf', 'n_clicks'),
    Input('btn-export-pdf', 'n_clicks'),
    prevent_initial_call=True
)
def export_pdf(n_clicks):
    if n_clicks:
        options = {'page-size': 'A4', 'encoding': 'UTF-8'}
        try:
            pdfkit.from_file('templates/layout.html', 'dashboard_dia_wine.pdf', configuration=config, options=options)
            print("PDF exportado com sucesso!")
        except Exception as e:
            print(f"Erro ao exportar PDF: {e}")
    return None

# Função para exportar Excel
@app.callback(
    Output('btn-export-excel', 'data'),
    Input('btn-export-excel', 'n_clicks'),
    prevent_initial_call=True
)
def export_excel(n_clicks):
    if n_clicks:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name="dashboard_dia_wine.xlsx")

# Função para exportar CSV
@app.callback(
    Output('btn-export-csv', 'data'),
    Input('btn-export-csv', 'n_clicks'),
    prevent_initial_call=True
)
def export_csv(n_clicks):
    if n_clicks:
        csv_string = df.to_csv(index=False)
        output = io.StringIO()
        output.write(csv_string)
        output.seek(0)
        return send_file(output, mimetype='text/csv', as_attachment=True, download_name="dashboard_dia_wine.csv")

# Rodar o app
if __name__ == '__main__':
    app.run_server(debug=True)

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import pdfkit

# Inicializando a aplicação
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Carregando os dados
df = pd.read_csv('seus_dados.csv')

# Função para exportar dados para Excel
def export_to_excel(filtered_df):
    filtered_df.to_excel('dados_exportados.xlsx', index=False)

# Função para exportar dados para CSV
def export_to_csv(filtered_df):
    filtered_df.to_csv('dados_exportados.csv', index=False)

# Layout da aplicação
app.layout = dbc.Container([
    html.H1('Dashboard - Dia Wine', style={'textAlign': 'center', 'color': '#FFFFFF'}),
    
    # Filtros simplificados
    dbc.Row([
        dbc.Col([html.Label("Cód. Cliente", style={'color': '#FFFFFF'}), 
                 dcc.Dropdown(id='filter-codcli',
                 options=[{'label': str(cod), 'value': cod} for cod in df['COD CLIENTE'].unique()],
                 multi=True)], width=2),
        
        dbc.Col([html.Label("Cód. Produto", style={'color': '#FFFFFF'}), 
                 dcc.Dropdown(id='filter-codprod',
                 options=[{'label': str(cod), 'value': cod} for cod in df['COD PROD'].unique()],
                 multi=True)], width=2),
        
        dbc.Col([html.Label("RCA", style={'color': '#FFFFFF'}), 
                 dcc.Dropdown(id='filter-rca',
                 options=[{'label': rca, 'value': rca} for rca in df['RCA'].unique()],
                 multi=True)], width=2),
        
        dbc.Col([html.Label("Departamento", style={'color': '#FFFFFF'}), 
                 dcc.Dropdown(id='filter-depto',
                 options=[{'label': dept, 'value': dept} for dept in df['DEPARTAMENTO'].unique()],
                 multi=True)], width=2),
        
        dbc.Col([html.Label("Data de Faturamento", style={'color': '#FFFFFF'}),
                 dcc.DatePickerRange(id='filter-dtfat', display_format="DD-MM-YYYY")], width=2),
        
        dbc.Col([html.Label("Seguimento", style={'color': '#FFFFFF'}),
                 dcc.Dropdown(id='filter-seguimento',
                 options=[{'label': seg, 'value': seg} for seg in df['SEGUIMENTO'].unique()],
                 multi=True)], width=2),
    ], className='mb-4'),

    # Gráficos
    dbc.Row([
        dbc.Col(dcc.Graph(id='vendas-grafico'), width=6),
        dbc.Col(dcc.Graph(id='clientes-grafico'), width=6)
    ]),
    
    dbc.Row([
        dbc.Col(dcc.Graph(id='positivacao-grafico'), width=6),
        dbc.Col(dcc.Graph(id='meta-vendas-grafico'), width=6),
        dbc.Col(dcc.Graph(id='tendencia-vendas-grafico'), width=6),
    ]),
    
    # Botões de exportação
    dbc.Row([
        dbc.Button("Exportar PDF", id="btn-export-pdf", color="primary", className="mt-3"),
        dbc.Button("Exportar Excel", id="btn-export-excel", color="secondary", className="mt-3 ml-3"),
        dbc.Button("Exportar CSV", id="btn-export-csv", color="secondary", className="mt-3 ml-3"),
    ]),
    
    # Exibição de alertas
    html.Div(id='alertas-meta-vendas')
    
], fluid=True, style={'backgroundColor': '#000000'})

# Callback para atualizar os gráficos
@app.callback(
    [Output('vendas-grafico', 'figure'),
     Output('clientes-grafico', 'figure'),
     Output('positivacao-grafico', 'figure'),
     Output('meta-vendas-grafico', 'figure'),
     Output('tendencia-vendas-grafico', 'figure')],
    [Input('filter-codcli', 'value'),
     Input('filter-codprod', 'value'),
     Input('filter-rca', 'value'),
     Input('filter-depto', 'value'),
     Input('filter-dtfat', 'start_date'),
     Input('filter-dtfat', 'end_date'),
     Input('filter-seguimento', 'value')]
)
def update_graphs(codcli, codprod, rca, depto, start_date, end_date, seguimento):
    filtered_df = df.copy()
    
    # Aplicando os filtros
    if codcli:
        filtered_df = filtered_df[filtered_df['COD CLIENTE'].isin(codcli)]
    if codprod:
        filtered_df = filtered_df[filtered_df['COD PROD'].isin(codprod)]
    if rca:
        filtered_df = filtered_df[filtered_df['RCA'].isin(rca)]
    if depto:
        filtered_df = filtered_df[filtered_df['DEPARTAMENTO'].isin(depto)]
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['DT FAT'] >= start_date) & (filtered_df['DT FAT'] <= end_date)]
    if seguimento:
        filtered_df = filtered_df[filtered_df['SEGUIMENTO'].isin(seguimento)]
    
    # Encurtar nomes de produtos
    filtered_df['PRODUTO'] = filtered_df['PRODUTO'].apply(lambda x: x[:15] + '...' if len(x) > 15 else x)
    
    # Gráficos simplificados
    vendas_fig = px.bar(filtered_df, x='PRODUTO', y='TOTAL', title='Vendas por Produto', text_auto=True)
    clientes_fig = px.bar(filtered_df, x='NOME FANTASIA', y='QT', title='Clientes por Produto', text_auto=True)
    positivacao_fig = px.line(filtered_df, x='DT FAT', y='QT', title='Positivação por Período', markers=True)
    meta_vendas_fig = px.bar(filtered_df, x='DEPARTAMENTO', y='TOTAL', title='Meta X Vendas', text_auto=True)
    
    # Gráfico de tendência de vendas
    tendencia_vendas_fig = px.line(filtered_df, x='DT FAT', y='TOTAL', title='Tendência de Vendas ao Longo do Tempo', markers=True)
    
    return vendas_fig, clientes_fig, positivacao_fig, meta_vendas_fig, tendencia_vendas_fig

# Callback para alertar metas de vendas atingidas
@app.callback(
    Output('alertas-meta-vendas', 'children'),
    [Input('filter-codprod', 'value')]
)
def alertar_metas_vendas(codprod):
    alertas = []
    for produto in codprod:
        total_vendas = df[df['COD PROD'] == produto]['TOTAL'].sum()
        meta = 10000  # Exemplo de meta
        if total_vendas >= meta:
            alertas.append(f'Meta de vendas atingida para o produto {produto}!')
    
    return [html.Div(alerta, style={'color': 'green'}) for alerta in alertas]

# Callback para exportar o PDF
@app.callback(
    Output('btn-export-pdf', 'n_clicks'),
    Input('btn-export-pdf', 'n_clicks'),
    prevent_initial_call=True
)
def export_pdf(n_clicks):
    if n_clicks:
        try:
            options = {'page-size': 'A4', 'encoding': 'UTF-8'}
            config = pdfkit.configuration(wkhtmltopdf=r'C:\Users\carol.barroso\Documents\GitHub\powerbi-diawine\wkhtmltopdf\bin\wkhtmltopdf.exe')
            pdfkit.from_file('templates/layout.html', 'dashboard_dia_wine.pdf', configuration=config, options=options)
            print("PDF exportado com sucesso!")
        except Exception as e:
            print(f"Erro ao exportar PDF: {e}")
    return None

# Callback para exportar Excel
@app.callback(
    Output('btn-export-excel', 'n_clicks'),
    Input('btn-export-excel', 'n_clicks'),
    prevent_initial_call=True
)
def export_excel(n_clicks):
    if n_clicks:
        try:
            export_to_excel(df)
            print("Dados exportados para Excel!")
        except Exception as e:
            print(f"Erro ao exportar Excel: {e}")
    return None

# Callback para exportar CSV
@app.callback(
    Output('btn-export-csv', 'n_clicks'),
    Input('btn-export-csv', 'n_clicks'),
    prevent_initial_call=True
)
def export_csv(n_clicks):
    if n_clicks:
        try:
            export_to_csv(df)
            print("Dados exportados para CSV!")
        except Exception as e:
            print(f"Erro ao exportar CSV: {e}")
    return None

# Rodar o app
if __name__ == '__main__':
    app.run_server(debug=True)

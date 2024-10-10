import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.io as pio

# Inicializar o app
app = dash.Dash(__name__)

# Carregar dados
df = pd.read_excel("dados_vendas.xlsx")

# Layout do app
app.layout = html.Div(
    style={'backgroundColor': '#151D52', 'color': '#FFFFFF', 'font-family': 'Arial, sans-serif'},
    children=[
        html.H1("Relatório Dia Wine", style={'textAlign': 'center', 'color': '#F6C62D'}),
        
        # Filtros
        html.Div([
            html.Label("Código do Cliente:"),
            dcc.Dropdown(
                id='filter-codcli',
                options=[{'label': str(cod), 'value': cod} for cod in df['COD CLIENTE'].unique()],
                multi=True
            ),
            html.Label("Código do Produto:"),
            dcc.Dropdown(
                id='filter-codprod',
                options=[{'label': str(prod), 'value': prod} for prod in df['COD PROD'].unique()],
                multi=True
            ),
            html.Label("RCA:"),
            dcc.Dropdown(
                id='filter-rca',
                options=[{'label': str(rca), 'value': rca} for rca in df['RCA'].unique()],
                multi=True
            ),
            html.Label("Departamento:"),
            dcc.Dropdown(
                id='filter-depto',
                options=[{'label': str(depto), 'value': depto} for depto in df['DEPARTAMENTO'].unique()],
                multi=True
            ),
            html.Label("Data de Faturamento:"),
            dcc.DatePickerRange(
                id='filter-dtfat',
                start_date=df['DT FAT'].min(),
                end_date=df['DT FAT'].max()
            ),
            html.Label("Seguimento:"),
            dcc.Dropdown(
                id='filter-seguimento',
                options=[{'label': seg, 'value': seg} for seg in df['SEGUIMENTO'].unique()],
                multi=True
            ),
        ], style={'width': '25%', 'display': 'inline-block', 'padding': '10px', 'backgroundColor': '#1E2747'}),
        
        # Gráficos
        html.Div([
            dcc.Graph(id='vendas-grafico'),
            dcc.Graph(id='clientes-grafico'),
            dcc.Graph(id='positivacao-grafico'),
            dcc.Graph(id='meta-vendas-grafico')
        ], style={'width': '70%', 'display': 'inline-block', 'padding': '10px'}),
    ]
)

# Função de callback para atualizar os gráficos
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
    clientes_fig = px.bar(filtered_df, x='NOME FANTASIA', y='QT', title='Clientes por Produto', text_auto=True)
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

# Executar o servidor
if __name__ == '__main__':
    app.run_server(debug=True)

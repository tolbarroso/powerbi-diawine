import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import pdfkit

# Carregar os dados da planilha Excel
df = pd.read_excel('planilhas/dados_dia_wine.xlsx', sheet_name='Vendas')

# Inicializando a aplicação Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Configure o caminho para o executável wkhtmltopdf
config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

# Layout do Dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Img(src=app.get_asset_url('logo.png'), height="60px"), width="auto"),
        dbc.Col(html.H1("Dashboard Dia Wine", style={'color': '#F6C62D', 'textAlign': 'center'}), width=True)
    ], justify="between", align="center", className='mb-4'),

    dbc.Row([
        dbc.Col([
            html.Label("RCA", style={'color': '#FFFFFF'}),
            dcc.Dropdown(
                id='filter-rca',
                options=[{'label': rca, 'value': rca} for rca in df['RCA'].unique() if pd.notna(rca)],
                multi=True,
                value=[]
            )
        ], width=3),

        dbc.Col([
            html.Label("Código do Cliente", style={'color': '#FFFFFF'}),
            dcc.Dropdown(
                id='filter-codigo-cliente',
                options=[{'label': str(cod), 'value': cod} for cod in df['Cod Cliente'].unique() if pd.notna(cod)],
                multi=True,
                value=[]
            )
        ], width=3),

        dbc.Col([
            html.Label("Data de Início", style={'color': '#FFFFFF'}),
            dcc.DatePickerSingle(id='filter-data-inicio', display_format="DD-MM-YYYY", placeholder="Data de Início")
        ], width=3),

        dbc.Col([
            html.Label("Data de Fim", style={'color': '#FFFFFF'}),
            dcc.DatePickerSingle(id='filter-data-fim', display_format="DD-MM-YYYY", placeholder="Data de Fim")
        ], width=3),
        
        dbc.Col([
            html.Label("Departamento", style={'color': '#FFFFFF'}),
            dcc.Dropdown(
                id='filter-departamento',
                options=[{'label': dep, 'value': dep} for dep in df['Departamento'].unique() if pd.notna(dep)],
                multi=True,
                value=[]
            )
        ], width=3),

        dbc.Col([
            html.Label("Fornecedor", style={'color': '#FFFFFF'}),
            dcc.Dropdown(
                id='filter-fornecedor',
                options=[{'label': forn, 'value': forn} for forn in df['Fornecedor'].unique() if pd.notna(forn)],
                multi=True,
                value=[]
            )
        ], width=3)
    ], className='mb-4'),

    # Gráficos
    dbc.Row([
        dbc.Col(dcc.Graph(id='vendas-grafico'), width=6),
        dbc.Col(dcc.Graph(id='clientes-grafico'), width=6),
    ], className='mb-4'),

    dbc.Row([
        dbc.Col(dcc.Graph(id='positivacao-grafico'), width=6),
        dbc.Col(dcc.Graph(id='meta-vendas-grafico'), width=6),
    ], className='mb-4'),

    dbc.Button("Exportar PDF", id="btn-export-pdf", color="primary"),
], fluid=True, style={'backgroundColor': '#151D52'})

# Callbacks para atualizar os gráficos e exportar PDF
@app.callback(
    [Output('vendas-grafico', 'figure'),
     Output('clientes-grafico', 'figure'),
     Output('positivacao-grafico', 'figure'),
     Output('meta-vendas-grafico', 'figure')],
    [Input('filter-rca', 'value'),
     Input('filter-codigo-cliente', 'value'),
     Input('filter-data-inicio', 'date'),
     Input('filter-data-fim', 'date'),
     Input('filter-departamento', 'value'),
     Input('filter-fornecedor', 'value')]
)
def update_graphs(selected_rcas, selected_clientes, start_date, end_date, selected_departamentos, selected_fornecedores):
    filtered_df = df

    # Aplicando os filtros
    if selected_rcas:
        filtered_df = filtered_df[filtered_df['RCA'].isin(selected_rcas)]
    if selected_clientes:
        filtered_df = filtered_df[filtered_df['Cod Cliente'].isin(selected_clientes)]
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['Data'] >= start_date) & (filtered_df['Data'] <= end_date)]
    if selected_departamentos:
        filtered_df = filtered_df[filtered_df['Departamento'].isin(selected_departamentos)]
    if selected_fornecedores:
        filtered_df = filtered_df[filtered_df['Fornecedor'].isin(selected_fornecedores)]

    # Gráficos atualizados com base nos filtros aplicados
    vendas_fig = px.line(filtered_df, x='Data', y='Valor', title="Valor Geral de Vendas")
    clientes_fig = px.pie(filtered_df, names='Cod Cliente', values='Qt. Vendida', title="Número de Clientes Compradores")
    positivacao_fig = px.scatter(filtered_df, x='Qt. Vendida', y='% Pos.', color='RCA', title="Positivação por Vendedor")
    meta_vendas_fig = px.bar(filtered_df, x='Data', y='Vl Meta', title="Meta X Vendas Reais Atuais")

    return vendas_fig, clientes_fig, positivacao_fig, meta_vendas_fig

@app.callback(
    Output('download-pdf', 'data'),
    [Input('btn-export-pdf', 'n_clicks')],
    prevent_initial_call=True
)
def export_pdf(n_clicks):
    pdf_file = 'report.pdf'
    pdfkit.from_file('templates/layout.html', pdf_file, configuration=config)
    return dcc.send_file(pdf_file)

if __name__ == '__main__':
    app.run_server(debug=True)

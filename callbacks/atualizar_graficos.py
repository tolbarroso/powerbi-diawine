import pandas as pd
from dash import Output, Input
from utils import gerar_comparativo, gerar_produtos_vendidos, gerar_ticket_medio, gerar_vendas_ano, gerar_vendas_mes

# Carrega os dados das diferentes abas da planilha Excel
df_vendas = pd.read_excel('dados_dia_wine.xlsx', sheet_name='Vendas_Mensal')
df_clientes = pd.read_excel('dados_dia_wine.xlsx', sheet_name='Clientes')
df_produtos = pd.read_excel('dados_dia_wine.xlsx', sheet_name='Produtos')
df_positivacao = pd.read_excel('dados_dia_wine.xlsx', sheet_name='Positivacao')
df_rca = pd.read_excel('dados_dia_wine.xlsx', sheet_name='RCA')
df_expectativas = pd.read_excel('dados_dia_wine.xlsx', sheet_name='Expectativas')

def registrar_callbacks(app):
    @app.callback(
        [Output('comparativo-periodo', 'figure'),
         Output('vendas-mes', 'figure'),
         Output('vendas-ano-passado', 'figure'),
         Output('produtos-mais-vendidos', 'figure'),
         Output('ticket-medio', 'figure')],
        [Input('filtro-equipe', 'value'),
         Input('filtro-rca', 'value'),
         Input('filtro-departamento', 'value'),
         Input('filtro-periodo', 'start_date'),
         Input('filtro-periodo', 'end_date')]
    )
    def atualizar_graficos(equipe, rca, departamento, start_date, end_date):
        # Filtra os dados de vendas para o período selecionado
        df_filtrado = df_vendas[(df_vendas['data'] >= start_date) & (df_vendas['data'] <= end_date)]

        # Aplica os filtros adicionais (equipe, rca, departamento)
        if equipe:
            df_filtrado = df_filtrado[df_filtrado['equipe'].isin(equipe)]
        if rca:
            df_filtrado = df_filtrado[df_filtrado['rca'].isin(rca)]
        if departamento:
            df_filtrado = df_filtrado[df_filtrado['departamento'].isin(departamento)]

        # Gera os gráficos filtrados
        comparativo_fig = gerar_comparativo(df_filtrado)
        vendas_mes_fig = gerar_vendas_mes(df_filtrado)
        vendas_ano_fig = gerar_vendas_ano(df_filtrado)
        
        # Para produtos mais vendidos, usamos a aba de produtos
        produtos_vendidos_fig = gerar_produtos_vendidos(df_produtos)
        
        # Gera o gráfico de ticket médio
        ticket_medio_fig = gerar_ticket_medio(df_filtrado)

        return comparativo_fig, vendas_mes_fig, vendas_ano_fig, produtos_vendidos_fig, ticket_medio_fig

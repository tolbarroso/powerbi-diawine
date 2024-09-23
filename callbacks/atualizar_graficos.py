import pandas as pd
from dash import Output, Input

# Carrega os dados da planilha
df = pd.read_excel('dados_dia_wine.xlsx')

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
        # Filtro dos dados
        df_filtrado = df[(df['data'] >= start_date) & (df['data'] <= end_date)]

        # Filtra com base nos dropdowns
        if equipe:
            df_filtrado = df_filtrado[df_filtrado['equipe'].isin(equipe)]
        if rca:
            df_filtrado = df_filtrado[df_filtrado['rca'].isin(rca)]
        if departamento:
            df_filtrado = df_filtrado[df_filtrado['departamento'].isin(departamento)]

        # Aqui, retornamos gráficos com base nos dados filtrados.
        comparativo_fig = gerar_comparativo(df_filtrado)
        vendas_mes_fig = gerar_vendas_mes(df_filtrado)
        vendas_ano_fig = gerar_vendas_ano(df_filtrado)
        produtos_vendidos_fig = gerar_produtos_vendidos(df_filtrado)
        ticket_medio_fig = gerar_ticket_medio(df_filtrado)

        return comparativo_fig, vendas_mes_fig, vendas_ano_fig, produtos_vendidos_fig, ticket_medio_fig

def gerar_comparativo(df):
    # Gera o gráfico comparativo entre períodos
    pass

def gerar_vendas_mes(df):
    # Gera o gráfico de vendas do mês
    pass

def gerar_vendas_ano(df):
    # Gera o gráfico de vendas do ano passado
    pass

def gerar_produtos_vendidos(df):
    # Gera o gráfico de produtos mais vendidos
    pass

def gerar_ticket_medio(df):
    # Gera o gráfico do ticket médio
    pass

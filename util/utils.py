import pandas as pd
import plotly.graph_objects as go

def carregar_dados(caminho_arquivo):
    """
    Carrega os dados da planilha Excel e retorna um DataFrame.
    """
    try:
        df = pd.read_excel(caminho_arquivo)
        return df
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

def gerar_comparativo(df):
    """
    Gera gráfico comparativo entre dois períodos.
    """
    # Exemplo: calcular vendas por mês
    comparativo = df.groupby(df['data'].dt.strftime('%Y-%m'))['vendas'].sum()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=comparativo.index,
        y=comparativo.values,
        name='Comparativo de Vendas'
    ))
    
    fig.update_layout(
        title='Comparativo Período x Período',
        xaxis_title='Mês',
        yaxis_title='Vendas',
        template='plotly_dark',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='#F6C62D')
    )
    
    return fig

def gerar_vendas_mes(df):
    """
    Gera gráfico de vendas do mês atual.
    """
    vendas_mes = df[df['data'].dt.month == pd.Timestamp.now().month]['vendas'].sum()

    fig = go.Figure(go.Indicator(
        mode="number",
        value=vendas_mes,
        title={"text": "Vendas do Mês Atual"},
        number={'prefix': "R$"},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))

    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='#F6C62D')
    )

    return fig

def gerar_vendas_ano(df):
    """
    Gera gráfico de vendas do ano anterior.
    """
    ano_anterior = pd.Timestamp.now().year - 1
    vendas_ano_anterior = df[df['data'].dt.year == ano_anterior]['vendas'].sum()

    fig = go.Figure(go.Indicator(
        mode="number",
        value=vendas_ano_anterior,
        title={"text": "Vendas do Ano Anterior"},
        number={'prefix': "R$"},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))

    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='#F6C62D')
    )

    return fig

def gerar_produtos_vendidos(df):
    """
    Gera gráfico dos produtos mais vendidos.
    """
    produtos_vendidos = df.groupby('produto')['vendas'].sum().sort_values(ascending=False).head(10)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=produtos_vendidos.index,
        y=produtos_vendidos.values,
        name='Produtos Mais Vendidos'
    ))

    fig.update_layout(
        title='Top 10 Produtos Mais Vendidos',
        xaxis_title='Produto',
        yaxis_title='Vendas',
        template='plotly_dark',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='#F6C62D')
    )

    return fig

def gerar_ticket_medio(df):
    """
    Gera gráfico do ticket médio acumulado.
    """
    df['ticket_medio'] = df['vendas'] / df['quantidade']
    ticket_medio_acumulado = df['ticket_medio'].mean()

    fig = go.Figure(go.Indicator(
        mode="number",
        value=ticket_medio_acumulado,
        title={"text": "Ticket Médio por Produto"},
        number={'prefix': "R$"},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))

    fig.update_layout(
        template='plotly_dark',
        plot_bgcolor='black',
        paper_bgcolor='black',
        font=dict(color='#F6C62D')
    )

    return fig

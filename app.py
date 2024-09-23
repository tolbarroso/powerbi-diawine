from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from layouts.layout_inicial import layout_inicial
from callbacks import atualizar_graficos, exportar_pdf

# Criação do app com 'suppress_callback_exceptions=True' para lidar com componentes gerados dinamicamente
app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Dashboard Dia Wine"  # Define o título da aba do navegador

# Define o layout do aplicativo sem a barra de navegação
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback para carregar o layout inicial ou exibir erro 404
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return layout_inicial()  # Certifique-se de que este layout contém os IDs corretos
    else:
        return html.H1('404 - Página não encontrada')  # Exibe mensagem de erro para rotas inválidas

# Registra os callbacks dos gráficos e da exportação de PDF
atualizar_graficos.registrar_callbacks(app)
exportar_pdf.registrar_callbacks(app)

# Inicia o servidor
if __name__ == '__main__':
    app.run_server(debug=True)

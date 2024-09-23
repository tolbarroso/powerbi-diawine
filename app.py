from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from layouts.layout_inicial import layout_inicial
from callbacks import atualizar_graficos, exportar_pdf

app = Dash(__name__)

# Define o layout do aplicativo
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Carrega o layout inicial
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return layout_inicial()
    else:
        return '404 - Página não encontrada'

# Registra os callbacks
atualizar_graficos.registrar_callbacks(app)
exportar_pdf.registrar_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)

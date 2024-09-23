from dash import Dash, dcc, html
from layouts.layout_inicial import layout_inicial
from callbacks import atualizar_graficos, exportar_pdf

app = Dash(__name__, external_stylesheets=['/assets/custom.css'])

# Define o layout do aplicativo
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback para mudar a página com base no pathname
@app.callback(
    output=Output('page-content', 'children'),
    inputs=[input('url', 'pathname')]
)
def display_page(pathname):
    return layout_inicial() if pathname == '/' else '404 - Página não encontrada'

# Registra os callbacks
atualizar_graficos.registrar_callbacks(app)
exportar_pdf.registrar_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)

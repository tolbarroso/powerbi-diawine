import pdfkit
from dash import Output, Input

def registrar_callbacks(app):
    @app.callback(
        Output('exportar-pdf', 'children'),
        [Input('exportar-pdf', 'n_clicks')]
    )
    def exportar_para_pdf(n_clicks):
        if n_clicks > 0:
            pdfkit.from_url('http://127.0.0.1:8050', 'dashboard_dia_wine.pdf')
            return "PDF exportado com sucesso!"
        return "Exportar para PDF"

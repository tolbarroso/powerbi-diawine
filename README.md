# Dia Wine Dashboard

## Descrição

O **Dia Wine Dashboard** é uma aplicação web interativa desenvolvida em Python utilizando o framework Dash. Este dashboard foi projetado para fornecer uma visualização clara e concisa de dados de vendas e desempenho, permitindo que os usuários filtrem as informações com base em diferentes parâmetros.

## Estrutura do Projeto
dia_wine_dashboard/ 

├── dados_dia_wine.xlsx # Planilha com dados de vendas 

├── app.py # Código principal da aplicação 

├── layouts/ # Contém os layouts da aplicação 

│      ├── layout_inicial.py # Layout inicial do dashboard 

│      └── filtros.py # Componentes de filtro 

├── callbacks/ # Contém os callbacks da aplicação 

│      ├── atualizar_graficos.py # Atualização dos gráficos

│      └── exportar_pdf.py # Exportação para PDF 

├── assets/ # Arquivos estáticos 

│      └── custom.css # Estilos personalizados 

└── requisitos.txt # Dependências do projeto


## Instalação

Para instalar e executar a aplicação, siga os passos abaixo:

1. **Clone o repositório:**

   ```bash
   git clone <url-do-repositorio>
   cd dia_wine_dashboard

2. **Crie um ambiente virtual:**
    ```bash
    python -m venv venv

3. **Ative o ambiente virtual:**
    ```bash
    No Windows:
    venv\Scripts\activate

4. **Instale as dependências:**
    ```bash
    pip install -r requisitos.txt

## Como Usar
1. **Execute a aplicação:**
    ```bash
    python app.py

2. **Acesse o dashboard:**
    ```bash
    Abra o navegador e vá para http://127.0.0.1:8050.

## Funcionalidades
Filtros Interativos: Permite a seleção de equipe, RCA, departamento e intervalo de datas.
    
Gráficos Dinâmicos: Visualize o comparativo entre períodos, vendas mensais, vendas do ano anterior, produtos mais vendidos e ticket médio.
    
Exportação em PDF: Exporte o dashboard atual para um arquivo PDF com um clique.

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir um pull request ou relatar problemas.

## Licença
Este projeto está sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.

Contato
Para mais informações, entre em contato através de carolbarrosowork@gmail.com.

Sinta-se à vontade para substituir `<https://github.com/tolbarroso/powerbi-diawine>` e o email pelo seu contato real. Se precisar de mais alguma coisa, é só avisar!

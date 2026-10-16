# Curry Company — Growth Dashboard

Dashboard interativo para análise operacional de um marketplace de entregas. O projeto transforma uma base com **45.593 registros** em indicadores sobre pedidos, entregadores, restaurantes, trânsito e tempo de entrega.

> Projeto demonstrativo de portfólio, desenvolvido com dados de finalidade educacional. Não representa uma operação comercial real.

## Demonstração

[Acessar a URL atual do dashboard](https://project-curry-company.streamlit.app/)

**Status verificado em 16/10/2026:** a URL responde, mas redireciona para a tela de autenticação do Streamlit. Antes da divulgação no portfólio, a publicação precisa ser revisada para permitir acesso público.

## Objetivo de negócio

Consolidar, em uma única aplicação, os principais indicadores necessários para acompanhar o desempenho de três frentes do marketplace:

- **Empresa:** volume diário e semanal, pedidos por trânsito, cidade e veículo, além da distribuição geográfica.
- **Entregadores:** perfil, avaliações, condição dos veículos e rankings de velocidade por cidade.
- **Restaurantes:** distância média, tempo de entrega e variações por cidade, pedido, trânsito e festival.

## Principais entregas

- Navegação por três visões de negócio.
- Filtros interativos por data, trânsito e cidade.
- Indicadores, tabelas, gráficos e mapa geográfico.
- Tratamento de valores ausentes, tipos de dados e campos textuais.
- Aplicação web responsiva publicada com Streamlit.

## Tecnologias

- Python
- Pandas e NumPy
- Streamlit
- Plotly e Folium
- Haversine

## Estrutura do projeto

```text
Curry-Company-Project-main/
├── Home.py
├── pages/
│   ├── 1_Visao_Empresa.py
│   ├── 2_Visao_Entregador.py
│   └── 3_Visao_Resturante.py
├── dataset/train.csv
├── logo.png
└── requirements.txt
```

## Executar localmente

```bash
git clone https://github.com/borges1411/curry_company.git
cd curry_company/Curry-Company-Project-main
python -m venv .venv
```

Ative o ambiente virtual, instale as dependências e execute o app:

```bash
pip install -r requirements.txt
streamlit run Home.py
```

## Recorte dos dados

- 45.593 registros brutos.
- Pedidos registrados entre fevereiro e abril de 2022.
- Variáveis operacionais de entrega, clima, trânsito, localização, veículo, restaurante e entregador.

## Aprendizados demonstrados

Este projeto evidencia competências em preparação de dados, definição de indicadores, visualização, análise exploratória e entrega de uma aplicação analítica acessível pela web.

## Próximas evoluções

- Centralizar a etapa de tratamento de dados para reduzir repetição entre páginas.
- Adicionar testes automatizados para as transformações e métricas.
- Padronizar todos os rótulos e indicadores em português.
- Criar uma página executiva com os KPIs prioritários e conclusões acionáveis.

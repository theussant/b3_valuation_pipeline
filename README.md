# B3 Valuation & Data Pipeline 📈

Este projeto é um pipeline de dados (ETL) e bot de monitoramento para o mercado financeiro brasileiro (B3). O sistema automatiza a coleta de preços, armazena em um banco relacional e aplica modelos de Valuation (como o Preço Justo de Graham) para identificar oportunidades de investimento.

## 🚀 Diferencial: Resiliência de Dados
O pipeline foi projetado com uma lógica de **fallback**. Caso a API do Yahoo Finance apresente instabilidade ou bloqueio (*Rate Limit*), o sistema automaticamente consome os dados históricos do banco de dados local para garantir a continuidade dos cálculos e relatórios visuais.

## 🛠️ Stack Tecnológica
- **Linguagem:** Python 3.11
- **Orquestração:** Docker & Docker Compose
- **Banco de Dados:** SQLite (com SQLAlchemy ORM)
- **Bibliotecas Principais:** Pandas, Matplotlib, Loguru, yfinance
- **Data Quality:** Pydantic

## 🏗️ Arquitetura do Sistema
1. **Extração:** Coleta dados históricos e atuais via `yfinance`.
2. **Carga:** Persistência dos dados brutos em banco SQLite.
3. **Transformação:** Processamento de indicadores fundamentalistas (LPA, VPA, Preço Justo).
4. **Visualização:** Geração automática de gráficos de análise técnica vs. valor justo na pasta `/reports`.

## 📦 Como Executar

### Pré-requisitos
- Docker e Docker Compose instalados.

### Passos para rodar o projeto:

1. Clone o repositório:
git clone https://github.com/theussant/b3-valuation-etl-pipeline.git

2. Acesse a pasta do projeto:
cd b3-valuation-etl-pipeline

3. Suba o container Docker:
docker-compose up -d --build

4. Execute o pipeline de monitoramento:
docker-compose exec app python main.py

---
Desenvolvido por [Matheus](https://github.com/theussant).
# B3 Valuation & Data Pipeline 📈

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-container-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Pipeline de dados (ETL) e bot de monitoramento para o mercado financeiro brasileiro (B3). O sistema automatiza a extração de preços via API oficial, armazena em banco relacional e aplica modelos de Valuation (Graham) para identificação de ativos abaixo do valor intrínseco.



## 🚀 Diferenciais Técnicos

* **Extração via API Oficial:** Migração completa de *scraping* para **Alpha Vantage API**, garantindo estabilidade e governança dos dados.
* **Segurança de Segredos:** Implementação de gestão de credenciais via variáveis de ambiente (`.env`).
* **Arquitetura Dockerizada:** Deploy simplificado com isolamento total de dependências.
* **Resiliência:** Lógica de *Rate Limit* integrada para respeitar os limites de chamadas da API gratuita (5 req/min).

---

## 🛠️ Stack Tecnológica

| Camada | Tecnologia |
| :--- | :--- |
| **Linguagem** | Python 3.11 |
| **Extração** | Requests (Alpha Vantage API) |
| **Orquestração** | Docker & Docker Compose |
| **Banco de Dados** | SQLite (SQLAlchemy ORM) |
| **Data Quality** | Pydantic |
| **Monitoramento** | Loguru |
| **Visualização** | Matplotlib |

---

## 🏗️ Fluxo do Pipeline (ETL)

1.  **Extract:** Coleta de séries temporais diárias via REST API da Alpha Vantage (sufixo `.SAO` para B3).
2.  **Load:** Persistência dos dados brutos em banco SQLite estruturado.
3.  **Transform:** Cálculo automático do **Preço Justo de Graham** baseado em indicadores fundamentalistas (LPA, VPA).
4.  **Visualize:** Geração de relatórios visuais comparativos (Preço vs. Valor Justo) na pasta `/reports`.



---

## 📦 Como Executar

### 1. Pré-requisitos
* Docker e Docker Compose instalados.
* Chave de API (Obtenha gratuitamente em [Alpha Vantage](https://www.alphavantage.co/support/#api-key)).

### 2. Configuração
Clone o repositório e prepare o arquivo de ambiente:
```bash
git clone [https://github.com/theussant/b3-valuation-etl-pipeline.git](https://github.com/theussant/b3-valuation-etl-pipeline.git)
cd b3-valuation-etl-pipeline
cp .env.example .env

### 3. Execução via Docker
Suba o ambiente e execute o pipeline através do container:

```bash
# Subir container em background
docker-compose up -d --build

# Rodar o pipeline de execução
docker exec -it b3_etl_container python main.py
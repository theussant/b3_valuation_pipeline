from src.database import db
from src.extract import AlphaVantageExtractor  # Mudamos de YFinance para AlphaVantage
from src.load import DataLoader
from src.transform import ValuationTransformer
from src.visualize import Visualizer 
from loguru import logger 
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (API Key)
load_dotenv()

# Log estruturado
logger.add("logs/pipeline.log", rotation="500 MB")

def run_pipeline(tickers_list):
    logger.info("Iniciando Pipeline de Valuation B3 (via Alpha Vantage API)...")

    # 1. SETUP: Tabelas
    db.create_tables()

    # 2. EXTRAÇÃO (Agora via API oficial Alpha Vantage)
    extractor = AlphaVantageExtractor()
    df_raw = extractor.fetch_prices(tickers_list)

    # Se a API falhar ou o limite de 5/min for atingido severamente
    if df_raw.empty:
        logger.error("Falha na extração. Verifique sua API Key no .env ou o limite de uso.")
        return

    # 3. CARGA
    loader = DataLoader()
    loader.load_prices(df_raw)

    # 4. TRANSFORMAÇÃO
    # Mapeamento de dados para cálculo de Graham
    market_data_map = {
        "PETR4.SA": {"lpa": 10.50, "vpa": 28.30, "last_12m_div": 4.50},
        "VALE3.SA": {"lpa": 8.20, "vpa": 45.10, "last_12m_div": 3.20},
        "ITUB4.SA": {"lpa": 3.40, "vpa": 19.80, "last_12m_div": 1.20}
    }

    transformer = ValuationTransformer()
    viz = Visualizer() 
    
    print("\n" + "="*50)
    print("MONITORAMENTO ATIVO - B3 (API ALPHA VANTAGE)")
    print("="*50)

    for ticker in tickers_list:
        ticker_sa = ticker if ticker.endswith(".SA") else f"{ticker}.SA"
        # Filtro DataFrame pelo ticker atual
        df_ticker = df_raw[df_raw['ticker'] == ticker_sa]
        
        if not df_ticker.empty and ticker_sa in market_data_map:
            result = transformer.process_valuation(df_ticker, market_data_map[ticker_sa])
            
            print(f"Ativo: {result['ticker']}")
            print(f"Preço Atual: R$ {result['last_price']}")
            print(f"Preço Justo (Graham): R$ {result['graham_fair_value']}")
            print(f"Status: {result['status']}")
            
            # 5. VISUALIZAÇÃO
            viz.create_valuation_plot(df_ticker, result['graham_fair_value'], ticker_sa)
            print("-" * 30)

    logger.success("Pipeline finalizado com sucesso!")

if __name__ == "__main__":
    # Tickers para monitoramento
    meus_ativos = ["PETR4", "VALE3", "ITUB4"]
    run_pipeline(meus_ativos)
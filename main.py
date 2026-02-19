from src.database import db
from src.extract import YFinanceExtractor
from src.load import DataLoader
from src.transform import ValuationTransformer
from src.visualize import Visualizer 
from loguru import logger # type: ignore
import sys

# Log estruturado
logger.add("logs/pipeline.log", rotation="500 MB")

def run_pipeline(tickers_list):
    logger.info("Iniciando Pipeline de Valuation B3...")

    # 1. SETUP: Tabelas
    db.create_tables()

    # 2. EXTRAÇÃO (Foco total na API Yahoo Finance)
    extractor = YFinanceExtractor(tickers_list)
    df_raw = extractor.fetch_prices(period="1mo")

    # Se a API bloquear, o código para aqui e avisa
    if df_raw.empty:
        logger.error("Yahoo Finance bloqueou o acesso. Tente novamente em 15-30 minutos ou troque de rede.")
        return

    # 3. CARGA
    loader = DataLoader()
    loader.load_prices(df_raw)

    # 4. TRANSFORMAÇÃO
    market_data_map = {
        "PETR4.SA": {"lpa": 10.50, "vpa": 28.30, "last_12m_div": 4.50},
        "VALE3.SA": {"lpa": 8.20, "vpa": 45.10, "last_12m_div": 3.20},
        "ITUB4.SA": {"lpa": 3.40, "vpa": 19.80, "last_12m_div": 1.20}
    }

    transformer = ValuationTransformer()
    viz = Visualizer() 
    
    print("\n" + "="*50)
    print("MONITORAMENTO ATIVO - B3")
    print("="*50)

    for ticker in tickers_list:
        ticker_sa = ticker if ticker.endswith(".SA") else f"{ticker}.SA"
        df_ticker = df_raw[df_raw['ticker'] == ticker_sa]
        
        if not df_ticker.empty and ticker_sa in market_data_map:
            result = transformer.process_valuation(df_ticker, market_data_map[ticker_sa])
            
            print(f"Ativo: {result['ticker']}")
            print(f"Preço Atual: R$ {result['last_price']}")
            print(f"Preço Justo (Graham): R$ {result['graham_fair_value']}")
            print(f"Status: {result['status']}")
            
            # 5. VISUALIZAÇÃO (Gerando o relatório visual se a extração deu certo)
            viz.create_valuation_plot(df_ticker, result['graham_fair_value'], ticker_sa)
            print("-" * 30)

    logger.success("Pipeline finalizado com sucesso!")

if __name__ == "__main__":
    # Liste aqui os tickers que deseja monitorar no próximo teste
    meus_ativos = ["PETR4", "VALE3", "ITUB4"]
    run_pipeline(meus_ativos)
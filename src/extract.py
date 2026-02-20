import requests
import pandas as pd
import time
import os
from loguru import logger
from typing import List
from dotenv import load_dotenv

# Garante que as variáveis do .env sejam carregadas
load_dotenv()

class AlphaVantageExtractor:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_KEY")
        self.base_url = "https://www.alphavantage.co/query"
        
        if not self.api_key:
            logger.error("API Key da Alpha Vantage não encontrada! Verifique seu arquivo .env")

    def fetch_prices(self, tickers: List[str]) -> pd.DataFrame:
        all_data = []

        for ticker in tickers:
            # Alpha Vantage usa .SAO para B3
            symbol = f"{ticker.replace('.SA', '')}.SAO"
            
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol,
                "apikey": self.api_key,
                "datatype": "json"
            }
            
            try:
                logger.info(f"Extraindo {ticker} via Alpha Vantage API...")
                response = requests.get(self.base_url, params=params)
                data = response.json()
                
                # Tratamento de Rate Limit (5 por minuto na conta free)
                if "Note" in data:
                    logger.warning(f"Limite de chamadas atingido. Aguardando 60 segundos...")
                    time.sleep(60)
                    response = requests.get(self.base_url, params=params)
                    data = response.json()

                if "Time Series (Daily)" in data:
                    ts = data["Time Series (Daily)"]
                    df = pd.DataFrame.from_dict(ts, orient='index')
                    df = df.astype(float)
                    df.index = pd.to_datetime(df.index)
                    
                    df = df.reset_index().rename(columns={
                        'index': 'date',
                        '4. close': 'adj_close',
                        '5. volume': 'volume'
                    })
                    
                    df['ticker'] = ticker if ticker.endswith('.SA') else f"{ticker}.SA"
                    df['date'] = df['date'].dt.tz_localize(None)
                    
                    all_data.append(df[['ticker', 'date', 'adj_close', 'volume']])
                    logger.success(f"Dados de {ticker} obtidos com sucesso!")
                    
                    # Pausa de 15 segundos entre tickers para não bater no limite de 5/min
                    time.sleep(15) 
                else:
                    msg = data.get('Error Message') or data.get('Information') or 'Erro desconhecido'
                    logger.error(f"Erro na API para {ticker}: {msg}")

            except Exception as e:
                logger.error(f"Falha na conexão com Alpha Vantage: {e}")
                
        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
import yfinance as yf
import pandas as pd
import time
from datetime import datetime, timedelta
from loguru import logger
from typing import List
import requests

class YFinanceExtractor:
    def __init__(self, tickers: List[str]):
        self.tickers = [t.upper() if t.endswith('.SA') else f"{t.upper()}.SA" for t in tickers]
        # Configura uma sessão com headers de navegador para evitar o bloqueio
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def fetch_prices(self, period: str = "1mo") -> pd.DataFrame:
        all_data = []

        for ticker in self.tickers:
            try:
                logger.info(f"Baixando dados de: {ticker}")
                
                # sessão configurada
                df = yf.download(
                    ticker, 
                    period=period, 
                    interval="1d", 
                    progress=False, 
                    auto_adjust=True,
                    session=self.session 
                )
                
                if df.empty:
                    logger.warning(f"Nenhum dado encontrado para {ticker}.")
                    continue
                
                df = df.reset_index()
                df['ticker'] = ticker
                df = df.rename(columns={'Date': 'date', 'Close': 'adj_close', 'Volume': 'volume'})
                
                all_data.append(df[['ticker', 'date', 'adj_close', 'volume']])
                
                # Pequena pausa para não ser bloqueado novamente
                time.sleep(5) 
                
            except Exception as e:
                logger.error(f"Erro ao extrair {ticker}: {e}")
                continue
        
        return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
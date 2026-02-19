import pandas as pd
import numpy as np
from loguru import logger

class ValuationTransformer:
    def __init__(self):
        pass

    def calculate_bazin(self, dividend_per_share: float, desired_yield: float = 0.06) -> float:
        """
        Calcula o Preço Justo segundo Décio Bazin.
        Fórmula: Preço Justo = Dividendos dos últimos 12 meses / Yield Desejado (6%)
        """
        if dividend_per_share <= 0:
            return 0.0
        return round(dividend_per_share / desired_yield, 2)

    def calculate_graham(self, lpa: float, vpa: float) -> float:
        """
        Calcula o Preço Justo segundo Benjamin Graham.
        Fórmula: Vi = sqrt(22.5 * LPA * VPA)
        """
        if lpa <= 0 or vpa <= 0:
            return 0.0
        
        # O número 22.5 vem da premissa de Graham (P/L de 15 * P/VP de 1.5)
        fair_value = np.sqrt(22.5 * lpa * vpa)
        return round(fair_value, 2)

    def process_valuation(self, df_prices: pd.DataFrame, ticker_info: dict):
        """
        Recebe os preços e um dicionário com info financeira (LPA, VPA, Dividendos)
        e retorna um resumo de valuation.
        """
        if df_prices.empty:
            return None

        last_price = df_prices.sort_values('date').iloc[-1]['adj_close']
        
        lpa = ticker_info.get('lpa', 0)
        vpa = ticker_info.get('vpa', 0)
        total_div = ticker_info.get('last_12m_div', 0)

        price_graham = self.calculate_graham(lpa, vpa)
        price_bazin = self.calculate_bazin(total_div)

        # Cálculo de Upside (Margem de Segurança)
        upside_graham = ((price_graham / last_price) - 1) * 100 if price_graham > 0 else 0

        result = {
            'ticker': df_prices['ticker'].iloc[0],
            'last_price': last_price,
            'graham_fair_value': price_graham,
            'bazin_fair_value': price_bazin,
            'upside_graham_pct': round(upside_graham, 2),
            'status': "OPORTUNIDADE" if last_price < price_graham else "CARO"
        }
        
        logger.info(f"Valuation calculado para {result['ticker']}: Graham R$ {price_graham}")
        return result
import matplotlib.pyplot as plt
import pandas as pd
from loguru import logger
import os

class Visualizer:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        # Cria a pasta de relatórios se não existir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def create_valuation_plot(self, df_prices: pd.DataFrame, valuation_price: float, ticker: str):
        """
        Gera um gráfico comparando o preço histórico com o preço justo.
        """
        if df_prices.empty:
            logger.warning(f"Sem dados para gerar gráfico de {ticker}")
            return

        plt.figure(figsize=(12, 6))
        
        # Plotando os preços de fechamento
        plt.plot(df_prices['date'], df_prices['adj_close'], label='Preço de Mercado', color='#1f77b4', linewidth=2)
        
        # Plotando a linha de Preço Justo (Graham ou Bazin)
        plt.axhline(y=valuation_price, color='r', linestyle='--', label=f'Preço Justo (Graham): R$ {valuation_price}')
        
        # Estilização do gráfico
        plt.fill_between(df_prices['date'], df_prices['adj_close'], valuation_price, 
                         where=(df_prices['adj_close'] < valuation_price), 
                         interpolate=True, color='green', alpha=0.1, label='Zona de Margem de Segurança')

        plt.title(f"Análise de Valuation: {ticker}", fontsize=16)
        plt.xlabel("Data")
        plt.ylabel("Preço (R$)")
        plt.legend()
        plt.grid(True, linestyle=':', alpha=0.6)
        
        # Salvando a imagem
        file_path = f"{self.output_dir}/{ticker}_valuation.png"
        plt.savefig(file_path)
        plt.close() # Fecha a figura para liberar memória
        
        logger.success(f"Gráfico gerado com sucesso: {file_path}")
        return file_path
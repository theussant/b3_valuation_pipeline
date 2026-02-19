import pandas as pd
from datetime import datetime, timedelta
from src.load import DataLoader

def generate_mock_data(ticker="PETR4.SA"):
    logger_msg = "Gerando dados sintéticos para destravar o desenvolvimento..."
    print(logger_msg)
    
    # Criando os últimos 10 dias de preços
    today = datetime.now()
    dates = [today - timedelta(days=i) for i in range(10)]
    
    mock_data = {
        'ticker': [ticker] * 10,
        'date': [d.date() for d in dates],
        'adj_close': [35.50, 35.80, 36.20, 34.90, 35.10, 36.00, 37.20, 36.80, 35.50, 35.00],
        'volume': [1000000] * 10,
        'extracted_at': [datetime.now()] * 10
    }
    
    return pd.DataFrame(mock_data)

if __name__ == "__main__":
    df_fake = generate_mock_data()
    loader = DataLoader()
    loader.load_prices(df_fake)
    print("Sucesso! Banco de dados populado com dados de teste.")
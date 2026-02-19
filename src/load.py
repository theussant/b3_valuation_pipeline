import pandas as pd
from sqlalchemy.dialects.sqlite import insert
from src.database import db, RawPrice
from loguru import logger

class DataLoader:
    def __init__(self):
        self.Session = db.SessionLocal

    def load_prices(self, df: pd.DataFrame):
        """
        Insere dados no banco usando a lógica de Upsert.
        """
        if df.empty:
            logger.warning("DataFrame vazio. Nada para carregar.")
            return

        # Convertemos o DataFrame para uma lista de dicionários (formato que o SQL entende)
        data_to_insert = df.to_dict(orient='records')
        
        # Iniciamos uma sessão com o banco
        session = self.Session()
        
        try:
            logger.info(f"Iniciando carga de {len(data_to_insert)} registros no banco...")
            
            for row in data_to_insert:
                # Lógica de Upsert específica para SQLite
                stmt = insert(RawPrice).values(row)
                stmt = stmt.on_conflict_do_update(
                    index_elements=['ticker', 'date'], # Chave Primária
                    set_={
                        'adj_close': stmt.excluded.adj_close,
                        'volume': stmt.excluded.volume,
                        'extracted_at': stmt.excluded.extracted_at
                    }
                )
                session.execute(stmt)
            
            session.commit()
            logger.success("Dados carregados com sucesso no banco de dados!")
            
        except Exception as e:
            session.rollback()
            logger.error(f"Erro ao carregar dados no banco: {e}")
            raise e
        finally:
            session.close()
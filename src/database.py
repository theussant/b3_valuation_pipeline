import os
from sqlalchemy import create_engine, Column, String, Float, DateTime, Date
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from loguru import logger

# 1. Definição da Base para o ORM
Base = declarative_base()

# 2. Modelo da Tabela de Preços (Bronze Layer)
class RawPrice(Base):
    __tablename__ = 'raw_prices'
    
    ticker = Column(String, primary_key=True)
    date = Column(Date, primary_key=True)
    adj_close = Column(Float, nullable=False)
    volume = Column(Float)
    extracted_at = Column(DateTime, default=datetime.now)

# 3. Gerenciador do Banco de Dados
class DatabaseManager:
    def __init__(self, db_url: str = "sqlite:///./data/b3_data.db"):
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        logger.info(f"Conexão preparada para: {db_url}")

    def create_tables(self):
        """Cria as tabelas no banco de dados se elas não existirem."""
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.success("Tabelas criadas/verificadas com sucesso!")
        except Exception as e:
            logger.error(f"Erro ao criar tabelas: {e}")

# Instância para uso
db = DatabaseManager()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import DATABASE_URL


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    """Cria uma sessão do banco de dados para cada requisição."""
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

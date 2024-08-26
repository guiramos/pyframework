from urllib.parse import quote_plus
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os
from contextlib import contextmanager

Base = declarative_base()


def create_engine_parameters(user, password, host, db_name):
    connection_string = f'postgresql://{user}:{quote_plus(password)}@{host}/{db_name}'
    return create_engine(connection_string, pool_size=5, max_overflow=10)


engine = create_engine_parameters(
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    db_name=os.getenv('DB_NAME', 'postgres')
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise
    finally:
        db.close()


# For use with FastAPI's dependency injection system
def get_db_dependency():
    with get_db() as session:
        yield session

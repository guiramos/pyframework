import os
from contextlib import contextmanager
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session


def create_engine_parameters(user: str, password: str, host: str, db_name: str, **kwargs):
    """Create a SQLAlchemy engine with the given connection parameters.
    
    Args:
        user: Database username
        password: Database password
        host: Database host
        db_name: Database name
        **kwargs: Additional parameters to pass to create_engine
        
    Returns:
        SQLAlchemy engine instance
    """
    connection_string = f'postgresql://{user}:{quote_plus(password)}@{host}/{db_name}'
    return create_engine(connection_string, **kwargs)


# Create engine using environment variables
engine = create_engine_parameters(
    user=os.getenv('DB_USER', os.getenv('DATABASE_USER', 'postgres')),
    password=os.getenv('DB_PASSWORD', os.getenv('DATABASE_PASSWORD', '')),
    host=os.getenv('DB_HOST', os.getenv('DATABASE_HOST', 'localhost')),
    db_name=os.getenv('DB_NAME', os.getenv('DATABASE_NAME', 'postgres')),
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db_session() -> Session:
    """Get a database session with context management.
    
    Yields:
        SQLAlchemy Session: A database session
        
    Example:
        with get_db_session() as session:
            # Use the session
            result = session.query(User).all()
    """
    session = SessionLocal()
    try:
        yield session
    except SQLAlchemyError as e:
        session.rollback()
        raise
    finally:
        session.close()


# For backward compatibility with existing code
get_db = get_db_session

def get_db_dependency():
    """Get a database session for FastAPI dependency injection.
    
    This is a convenience wrapper around get_db_session for use with FastAPI's Depends.
    """
    with get_db_session() as session:
        yield session

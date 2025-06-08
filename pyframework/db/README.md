# Database Package

This package provides database utilities for SQLAlchemy-based applications, including base entities, repositories, and session management.

## Features

- **Session Management**: Easy database session handling with context managers
- **Base Entities**: Common base classes for database models
- **Repository Pattern**: Generic and specific repositories for common CRUD operations
- **Type Annotations**: Full type hints for better IDE support and code quality

## Installation

Add this package to your project's dependencies. The package requires:

- Python 3.10+
- SQLAlchemy 2.0+
- PostgreSQL (or any other SQLAlchemy-supported database)

## Usage

### Session Management

```python
from pyframework.db import get_db_session, SessionLocal

# Using as a context manager
with get_db_session() as session:
    # Use the session
    user = session.query(User).first()

# For FastAPI dependency injection
from fastapi import Depends
from pyframework.db import get_db_dependency

@app.get("/users/{user_id}")
async def get_user(user_id: str, db: Session = Depends(get_db_dependency)):
    return db.query(User).filter(User.id == user_id).first()
```

### Base Entities

```python
from sqlalchemy import Column, String
from pyframework.db.entities import BaseEntity

class UserEntity(BaseEntity):
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String)
```

### Repositories

```python
from pyframework.db.repositories import BaseRepository
from .models import UserEntity

class UserRepository(BaseRepository[UserEntity]):
    def __init__(self, db):
        super().__init__(db, UserEntity)
    
    def find_by_email(self, email: str) -> Optional[UserEntity]:
        return self.db.query(self.model).filter(self.model.email == email).first()

# Usage
with get_db_session() as session:
    repo = UserRepository(session)
    user = repo.find_by_email("user@example.com")
```

## Configuration

Set the following environment variables:

- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host
- `DB_NAME`: Database name

Or override the database URL directly by setting `DATABASE_URL`.

## Best Practices

1. Always use the context manager (`with get_db_session()`) to ensure proper session handling
2. Extend `BaseEntity` for your database models to get common fields like `created` and `updated`
3. Use the repository pattern for database operations to keep your code organized and testable
4. Always type hint your repository methods for better IDE support

## Testing

For testing, you can use an in-memory SQLite database:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create an in-memory SQLite database for testing
test_engine = create_engine('sqlite:///:memory:')
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Override the get_db_session dependency in your tests
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
```

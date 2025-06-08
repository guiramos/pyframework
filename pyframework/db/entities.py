import enum
from typing import TypeVar, Type, Optional, List, Any, Dict

from pydantic import BaseModel
from sqlalchemy import Column, String, Enum, DateTime, text, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Base class for all database entities
Base = declarative_base()

T = TypeVar('T')


class BaseEntity(Base):
    """Base class for all database entities with common fields.
    
    Attributes:
        created: Timestamp when the record was created
        updated: Timestamp when the record was last updated
    """
    __abstract__ = True
    
    created = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP'),
        doc='Timestamp when the record was created'
    )
    updated = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=text('CURRENT_TIMESTAMP'),
        doc='Timestamp when the record was last updated'
    )


class ProviderType(enum.Enum):
    """Enumeration of supported identity providers."""
    GOOGLE = "GOOGLE"
    MICROSOFT = "MICROSOFT"
    NONE = "NONE"


class StatusType(enum.Enum):
    """Enumeration of user status types."""
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    INACTIVE = "INACTIVE"


def from_model(model_instance: BaseModel, target_class: Type[T]) -> T:
    """Convert a Pydantic model instance to a SQLAlchemy model instance.
    
    Args:
        model_instance: Instance of a Pydantic model
        target_class: SQLAlchemy model class to convert to
        
    Returns:
        Instance of the target SQLAlchemy model class
    """
    target_instance = target_class()
    for field, value in model_instance.model_dump().items():
        setattr(target_instance, field, value)
    return target_instance


def to_model(
    entity_instance: BaseEntity, 
    target_model_class: Type[BaseModel],
    exclude_fields: Optional[List[str]] = None,
    dump: bool = False
) -> Any:
    """Convert a SQLAlchemy model instance to a Pydantic model instance.
    
    Args:
        entity_instance: SQLAlchemy model instance
        target_model_class: Pydantic model class to convert to
        exclude_fields: List of field names to exclude from conversion
        dump: If True, return a dictionary instead of a model instance
        
    Returns:
        Instance of the target Pydantic model class or a dictionary if dump=True
    """
    exclude_fields = exclude_fields or []
    model_data = {
        field: getattr(entity_instance, field) 
        for field in entity_instance.__table__.columns.keys() 
        if field not in exclude_fields
    }
    
    model_instance = target_model_class(**model_data)
    return model_instance.model_dump(exclude_unset=True, exclude_none=True) if dump else model_instance


class UserEntity(BaseEntity):
    """User entity representing a system user."""
    __tablename__ = 'users'
    __table_args__ = {'schema': 'core'}

    user_id = Column(String, primary_key=True, doc='Unique identifier for the user')
    email = Column(String, nullable=False, unique=True, doc='User email address (must be unique)')
    password = Column(String, nullable=True, doc='Hashed password (nullable for OAuth users)')
    first_name = Column(String, nullable=False, doc='User first name')
    last_name = Column(String, nullable=False, doc='User last name')
    provider = Column(Enum(ProviderType), nullable=False, doc='Authentication provider')
    status = Column(Enum(StatusType), nullable=False, default=StatusType.PENDING, doc='User account status')
    personal_data = Column(String, doc='Additional personal data (JSON string)')
    token = Column(String, doc='Temporary token for email verification/password reset')

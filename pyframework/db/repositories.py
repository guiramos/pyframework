from datetime import datetime, date
from typing import Optional, List, TypeVar, Type, Any, Dict, Generic

from sqlalchemy import func, cast, DateTime, and_, or_
from sqlalchemy.orm import Session, joinedload, Query

from .entities import BaseEntity, UserEntity, StatusType

T = TypeVar('T', bound=BaseEntity)

class BaseRepository(Generic[T]):
    """Base repository class providing common CRUD operations.
    
    This class should be subclassed for each entity type to provide
    type hints and custom query methods.
    
    Attributes:
        model: SQLAlchemy model class
        db: Database session
    """
    
    def __init__(self, db: Session, model: Type[T]):
        """Initialize the repository with a database session and model class.
        
        Args:
            db: SQLAlchemy database session
            model: SQLAlchemy model class
        """
        self.db = db
        self.model = model
    
    def save(self, entity: T) -> T:
        """Save an entity to the database.
        
        Args:
            entity: Entity to save
            
        Returns:
            The saved entity
        """
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def save_all(self, entities: List[T]) -> List[T]:
        """Save multiple entities to the database.
        
        Args:
            entities: List of entities to save
            
        Returns:
            List of saved entities
        """
        self.db.add_all(entities)
        self.db.commit()
        for entity in entities:
            self.db.refresh(entity)
        return entities
    
    def find_by_id(self, id: Any) -> Optional[T]:
        """Find an entity by its primary key.
        
        Args:
            id: Primary key value
            
        Returns:
            The found entity or None if not found
        """
        return self.db.query(self.model).get(id)
    
    def find_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Find all entities with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of entities
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def delete(self, entity: T) -> None:
        """Delete an entity from the database.
        
        Args:
            entity: Entity to delete
        """
        self.db.delete(entity)
        self.db.commit()
    
    def count(self) -> int:
        """Count the total number of entities.
        
        Returns:
            Total count of entities
        """
        return self.db.query(self.model).count()
    
    def exists_by_id(self, id: Any) -> bool:
        """Check if an entity with the given ID exists.
        
        Args:
            id: Primary key value
            
        Returns:
            True if entity exists, False otherwise
        """
        return self.db.query(self.model).get(id) is not None


class UserRepository(BaseRepository[UserEntity]):
    """Repository for User entities with user-specific queries."""
    
    def __init__(self, db: Session):
        """Initialize the repository.
        
        Args:
            db: SQLAlchemy database session
        """
        super().__init__(db, UserEntity)
    
    def find_by_email(self, email: str) -> Optional[UserEntity]:
        """Find a user by email address.
        
        Args:
            email: Email address to search for
            
        Returns:
            User entity if found, None otherwise
        """
        return self.db.query(UserEntity).filter(UserEntity.email == email).first()
    
    def exists_by_email(self, email: str) -> bool:
        """Check if a user with the given email exists.
        
        Args:
            email: Email address to check
            
        Returns:
            True if a user with the email exists, False otherwise
        """
        return self.db.query(UserEntity).filter(UserEntity.email == email).first() is not None
    
    def find_by_status(self, status: StatusType) -> List[UserEntity]:
        """Find all users with the given status.
        
        Args:
            status: Status to filter by
            
        Returns:
            List of users with the specified status
        """
        return self.db.query(UserEntity).filter(UserEntity.status == status).all()
    
    def update_name_and_personal_data(
        self, 
        user_id: str, 
        first_name: str, 
        last_name: str, 
        personal_data: Optional[str] = None
    ) -> bool:
        """Update a user's name and personal data.
        
        Args:
            user_id: ID of the user to update
            first_name: New first name
            last_name: New last name
            personal_data: Optional personal data (JSON string)
            
        Returns:
            True if the update was successful, False if user not found
        """
        result = self.db.query(UserEntity).filter(UserEntity.user_id == user_id).update({
            UserEntity.first_name: first_name,
            UserEntity.last_name: last_name,
            UserEntity.personal_data: personal_data
        })
        self.db.commit()
        return result > 0
    
    def find_by_email_and_token(self, email: str, token: str) -> Optional[UserEntity]:
        """Find a user by email and verification token.
        
        Args:
            email: User's email address
            token: Verification token
            
        Returns:
            User entity if found and token matches, None otherwise
        """
        return (
            self.db.query(UserEntity)
            .filter(
                and_(
                    UserEntity.email == email,
                    UserEntity.token == token
                )
            )
            .first()
        )

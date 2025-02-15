from typing import Optional
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel

# ------------------------
# Pydantic Models for Request and Response
# ------------------------

class Item(BaseModel):
    """
    Pydantic model representing an item response.
    This is used for API responses when retrieving or modifying an item.
    """
    id: int
    name: str
    description: Optional[str]

class ItemCreate(BaseModel):
    """
    Pydantic model for creating a new item.
    Used in POST requests.
    """
    name: str
    description: Optional[str]

class ItemUpdate(BaseModel):
    """
    Pydantic model for updating an existing item.
    Used in PUT requests. Fields are optional.
    """
    name: Optional[str]
    description: Optional[str]

# ------------------------
# Database Configuration
# ------------------------

DATABASE_URL = "sqlite:///test.db"  # SQLite database connection URL

# Define a base class for SQLAlchemy ORM models
class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass

class DBItem(Base):
    """
    SQLAlchemy ORM model representing the 'items' table.
    This model maps to the database table and is used for database operations.
    """
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)  # Auto-increment primary key
    name: Mapped[str] = mapped_column(String(30))  # Name with max length 30
    description: Mapped[Optional[str]]  # Optional description

# Create an SQLite engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize FastAPI application
app = FastAPI()

# ------------------------
# Database Dependency
# ------------------------

def get_db():
    """
    Dependency to create and manage a database session.
    It ensures the session is closed after the request is completed.
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

# ------------------------
# Event: Create Database Tables on Startup
# ------------------------

@app.on_event("startup")
async def startup():
    """
    Creates all database tables when the FastAPI application starts.
    """
    Base.metadata.create_all(bind=engine)

# ------------------------
# API Endpoints
# ------------------------

@app.post("/items", response_model=Item)
def create_item(item: ItemCreate, db: Session = Depends(get_db)) -> Item:
    """
    Create a new item in the database.
    
    - **item**: Request body containing 'name' and optional 'description'
    - **Returns**: Created item with an assigned ID
    """
    db_item = DBItem(**item.model_dump())  # Convert Pydantic model to SQLAlchemy model
    db.add(db_item)
    db.commit()
    db.refresh(db_item)  # Refresh to get the new ID
    return Item(**db_item.__dict__)  # Convert to response model

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    """
    Retrieve an item by its ID.
    
    - **item_id**: The ID of the item to retrieve
    - **Returns**: The item if found, otherwise raises a 404 error
    """
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return Item(**db_item.__dict__)

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)) -> Item:
    """
    Update an existing item.
    
    - **item_id**: The ID of the item to update
    - **item**: Request body with updated fields (name, description)
    - **Returns**: The updated item, otherwise raises a 404 error if not found
    """
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for key, value in item.model_dump().items():
        if value is not None:
            setattr(db_item, key, value)  # Update only provided fields
    
    db.commit()
    db.refresh(db_item)
    return Item(**db_item.__dict__)

@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> Item:
    """
    Delete an item from the database.
    
    - **item_id**: The ID of the item to delete
    - **Returns**: The deleted item, otherwise raises a 404 error if not found
    """
    db_item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return Item(**db_item.__dict__)

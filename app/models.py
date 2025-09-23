from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Users credentials
    email = Column(String(255), unique=True, index=True,nullable=False)
    hashed_password = Column(String(255), nullable=False)

    # Master key for encrypting/decrypting passwords
    master_key = Column(String(255), nullable=False)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    # Relationship to passwords
    passwords = relationship("Password", back_populates="owner")

class Password(Base):
    __tablename__ = "passwords"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key to link to User
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Password details
    service_name = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False)
    encrypted_password = Column(Text, nullable=False)
    
    # Optional notes
    url = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to User
    owner = relationship("User", back_populates="passwords")


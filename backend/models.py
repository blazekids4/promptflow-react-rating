from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import  relationship, Mapped
from typing import List, Optional
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = Column(Integer, primary_key=True)
    username: Mapped[str] = Column(String(30), unique=True)  # New username field
    name: Mapped[str] = Column(String(30))
    fullname: Mapped[Optional[str]] = Column(String(30), nullable=True)
    email: Mapped[str] = Column(String(30))
    password_hash: Mapped[str] = Column(String(528))  # Store hashed passwords
    organization: Mapped[str] = Column(String(30))
    role: Mapped[str] = Column(Enum('hr-compliance', 'hr-employee-relations', 'hr-recruiting', name='user_roles'))
    chat_sessions: Mapped[List["ChatSession"]] = relationship("ChatSession", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(ForeignKey("users.id"))
    created_at: Mapped[DateTime] = Column(DateTime)
    updated_at: Mapped[DateTime] = Column(DateTime)
    user: Mapped[User] = relationship("User", back_populates="chat_sessions")
    chat_messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    id: Mapped[int] = Column(Integer, primary_key=True)
    session_id: Mapped[int] = Column(ForeignKey('chat_sessions.id'))
    message_type: Mapped[str] = Column(Enum('user_input', 'llm_response', name='message_types'))
    content: Mapped[str] = Column(String)
    created_at: Mapped[DateTime] = Column(DateTime)
    session: Mapped[ChatSession] = relationship("ChatSession", back_populates="chat_messages")
    ratings: Mapped[List["Rating"]] = relationship("Rating", back_populates="message")

class Rating(db.Model):
    __tablename__ = 'ratings'
    id: Mapped[int] = Column(Integer, primary_key=True)
    message_id: Mapped[int] = Column(ForeignKey('chat_messages.id'))
    rating: Mapped[bool] = Column(Boolean)
    message: Mapped[ChatMessage] = relationship("ChatMessage", back_populates="ratings")


User.chat_sessions = relationship("ChatSession", order_by=ChatSession.id, back_populates="user")
ChatSession.chat_messages = relationship("ChatMessage", order_by=ChatMessage.id, back_populates="session")
ChatMessage.ratings = relationship("Rating", order_by=Rating.id, back_populates="message")

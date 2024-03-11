from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class PromptResponse(Base):
    __tablename__ = 'prompts_responses'

    id = Column(Integer, primary_key=True)
    user_prompt = Column(Text, nullable=False)
    llm_response = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True)
    prompt_response_id = Column(Integer, ForeignKey('prompts_responses.id'), nullable=False)
    thumbs_up = Column(Boolean)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())

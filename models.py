from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String, index=True)
    bot_response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

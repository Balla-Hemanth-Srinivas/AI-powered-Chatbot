from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

import models
from database import engine, get_db
from chatbot import chatbot

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Chatbot")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class InteractionLog(BaseModel):
    user_message: str
    bot_response: str
    timestamp: str

    class Config:
        orm_mode = True

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    user_msg = request.message
    bot_resp = chatbot.get_response(user_msg)

    # Log interaction
    db_interaction = models.Interaction(user_message=user_msg, bot_response=bot_resp)
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)

    return ChatResponse(response=bot_resp)

@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    interactions = db.query(models.Interaction).order_by(models.Interaction.timestamp.desc()).limit(50).all()
    return interactions

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Chatbot API. Serve static/index.html for UI."}

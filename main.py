import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from Bard import Chatbot
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://name-meaning-finder.vercel.app",
    "http://name-meaning-finder.vercel.app",
    "https://name-meaning-finder-git-master-mazilkhatib001-gmailcom.vercel.app",
    "http://name-meaning-finder-git-master-mazilkhatib001-gmailcom.vercel.app",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    session_id: str
    message: str


@app.post("/ask")
async def ask(request: Request, message: Message) -> dict:
    # Get the user-defined auth key from the environment variables
    user_auth_key = os.getenv('USER_AUTH_KEY')
    
    # Check if the user has defined an auth key,
    # If so, check if the auth key in the header matches it.
    if user_auth_key and user_auth_key != request.headers.get('Authorization'):
        raise HTTPException(status_code=401, detail='Invalid authorization key')

    # Execute your code without authenticating the resource
    chatbot = Chatbot(message.session_id)
    response = chatbot.ask(message.message)
    return response

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import anthropic
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal
import logging
import uvicorn

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Mastermind AI API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Valid model identifiers
MODELS = {
    "claude-3-haiku": "claude-3-haiku-20240307",
    "claude-3-sonnet": "claude-3-sonnet-20240229",  # Full version required
    "claude-3-opus": "claude-3-opus-20240229"  # Full version required
}

# Request models
class ChatRequest(BaseModel):
    message: str
    context: str = ""

class CodeGenerationRequest(BaseModel):
    prompt: str
    language: str = "python"

class MessageRequest(BaseModel):
    apiKey: str = Field(default="")
    message: str
    context: str = ""
    model: Literal["claude-3-haiku", "claude-3-sonnet", "claude-3-opus"] = "claude-3-sonnet"

# Chat Endpoint
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        logger.debug(f"Received chat request: {request}")
        response = client.messages.create(
            model=MODELS["claude-3-opus"],
            max_tokens=1000,
            messages=[
                {"role": "user", "content": request.message}
            ]
        )
        logger.debug("Chat processed successfully")
        return {"response": response.content[0].text}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Code Generation Endpoint
@app.post("/generate-code")
async def generate_code_endpoint(request: CodeGenerationRequest):
    try:
        logger.debug(f"Received code generation request: {request}")
        response = client.messages.create(
            model=MODELS["claude-3-opus"],
            max_tokens=1000,
            messages=[
                {"role": "user", "content": f"Generate a code snippet in {request.language} for the following task: {request.prompt}"}
            ]
        )
        logger.debug("Code generation processed successfully")
        return {"code": response.content[0].text}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Process Message Endpoint
@app.post("/process_message")
async def process_message(request: MessageRequest):
    try:
        logger.debug(f"Received message request: {request}")

        # Use API key from request or environment
        api_key = request.apiKey or os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            logger.error("No API key provided")
            raise HTTPException(status_code=401, detail="No API key provided")

        # Log API key (without revealing full key)
        logger.debug(f"Using API key ending with: {api_key[-5:]}")

        client = anthropic.Anthropic(api_key=api_key)
        
        # Combine context and message
        full_context = request.context + "\n\n" + request.message if request.context else request.message
        
        # Get model string
        model_version = MODELS.get(request.model)
        if not model_version:
            raise HTTPException(status_code=400, detail=f"Invalid model: {request.model}")
        
        logger.debug(f"Sending message to model: {model_version}")
        
        response = client.messages.create(
            model=model_version,
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": full_context
                }
            ]
        )
        
        logger.debug("Message processed successfully")
        
        return {
            "content": response.content[0].text,
            "memories": []  # Placeholder for future memory generation
        }
    except anthropic.APIError as e:
        logger.error(f"Anthropic API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Anthropic API Error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# Health Check
@app.get("/health")
async def health_check():
    logger.debug("Health check request received")
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
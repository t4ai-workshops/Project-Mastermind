import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import anthropic
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal, Optional, List
import logging
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Mastermind AI API",
    description="API for Mastermind AI Assistant using Anthropic's Claude models",
    version="0.1.0"
)

# CORS configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if allowed_origins != [""] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    context: str = ""

class CodeGenerationRequest(BaseModel):
    prompt: str
    language: str = "python"
    context: Optional[str] = None

class MessageRequest(BaseModel):
    apiKey: str = Field(default="")
    message: str
    context: str = ""
    model: Literal["claude-3-sonnet", "claude-3-opus", "claude-3-haiku"] = "claude-3-sonnet"

class Memory(BaseModel):
    content: str
    category: str
    importance: float

class ProcessResponse(BaseModel):
    content: str
    memories: List[Memory] = []

# Dependency for Anthropic client
def get_anthropic_client(api_key: Optional[str] = None):
    client_api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
    if not client_api_key:
        raise HTTPException(
            status_code=401,
            detail="No API key provided. Set ANTHROPIC_API_KEY in environment or provide in request."
        )
    return anthropic.Anthropic(api_key=client_api_key)

@app.post("/chat", response_model=ProcessResponse)
async def chat_endpoint(
    request: ChatRequest,
    client: anthropic.Anthropic = Depends(get_anthropic_client)
):
    try:
        logger.debug(f"Received chat request: {request}")
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": request.message}
            ]
        )
        logger.debug("Chat processed successfully")
        return ProcessResponse(
            content=response.content[0].text,
            memories=[]
        )
    except anthropic.APIError as e:
        logger.error(f"Anthropic API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-code", response_model=ProcessResponse)
async def generate_code_endpoint(
    request: CodeGenerationRequest,
    client: anthropic.Anthropic = Depends(get_anthropic_client)
):
    try:
        logger.debug(f"Received code generation request: {request}")
        
        # Build prompt with context if provided
        prompt = f"Generate a code snippet in {request.language} for the following task: {request.prompt}"
        if request.context:
            prompt = f"Context:\n{request.context}\n\n{prompt}"
        
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        logger.debug("Code generation processed successfully")
        return ProcessResponse(
            content=response.content[0].text,
            memories=[]
        )
    except anthropic.APIError as e:
        logger.error(f"Anthropic API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process_message", response_model=ProcessResponse)
async def process_message(request: MessageRequest):
    try:
        logger.debug(f"Received message request for model: {request.model}")
        
        # Get client using provided or environment API key
        client = get_anthropic_client(request.apiKey)
        
        # Combine context and message if context provided
        full_context = request.context + "\n\n" + request.message if request.context else request.message
        
        response = client.messages.create(
            model=request.model,
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": full_context
                }
            ]
        )
        
        logger.debug("Message processed successfully")
        
        return ProcessResponse(
            content=response.content[0].text,
            memories=[]  # Placeholder for future memory generation
        )
    except anthropic.APIError as e:
        logger.error(f"Anthropic API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint that also verifies API key configuration"""
    try:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        return {
            "status": "healthy",
            "api_configured": bool(api_key)
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="debug" if debug else "info"
    )
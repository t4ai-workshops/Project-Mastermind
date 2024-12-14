import os

# Stel de milieuvariabele in om parallelisme waarschuwingen te onderdrukken
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import anthropic
from fastapi.middleware.cors import CORSMiddleware
from typing import Literal, List, Dict, Any
import logging
import uvicorn

# Nieuwe imports
from mastermind.knowledge_cluster import KnowledgeCluster
from mastermind.vectordb import VectorEntry
from mastermind.mcp import MCPManager
from mastermind.database import add_memory, get_memories_by_category

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Mastermind AI API")

# Initialize Knowledge Cluster
knowledge_cluster = KnowledgeCluster()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Valid model identifiers
MODELS = {
    "claude-3-haiku": "claude-3-haiku-20240307",
    "claude-3-sonnet": "claude-3-sonnet-20240229",
    "claude-3-opus": "claude-3-opus-20240229"
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

class MemoryManagementRequest(BaseModel):
    entry_id: str
    importance: float
    memory_type: Literal["short_term", "long_term", "context"] = "long_term"

# Chat Endpoint met geheugen integratie
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        logger.debug(f"Received chat request: {request}")
        
        # Voeg een nieuwe herinnering toe
        add_memory(content="Voorbeeld content", category="chat_response", importance=0.5)
        
        # Haal herinneringen op
        memories = get_memories_by_category("chat_response")
        logger.debug(f"Retrieved memories: {memories}")
        
        # Zoek relevante herinneringen
        relevant_memories = await knowledge_cluster.retrieve_knowledge(
            query=request.message,
            max_results=3
        )
        logger.debug(f"Relevant memories: {relevant_memories}")
        
        # Bereid context voor met herinneringen
        enhanced_context = "\n\n".join([
            f"Relevante herinnering: {memory.metadata.get('content', '')}" 
            for memory in relevant_memories
        ]) + f"\n\nOorspronkelijke bericht: {request.message}"
        logger.debug(f"Enhanced context: {enhanced_context}")
        
        response = client.messages.create(
            model=MODELS["claude-3-opus"],
            max_tokens=1000,
            messages=[
                {"role": "user", "content": enhanced_context}
            ]
        )
        logger.debug(f"API Response: {response.content[0].text}")
        
        # Sla nieuwe kennis op
        await knowledge_cluster.store_knowledge(
            content=response.content[0].text,
            category='chat_response',
            importance=0.6
        )
        
        logger.debug("Chat processed successfully")
        return {
            "response": response.content[0].text,
            "memories": [memory.metadata for memory in relevant_memories]
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Code Generation Endpoint met geheugen context
@app.post("/generate-code")
async def generate_code_endpoint(request: CodeGenerationRequest):
    try:
        logger.debug(f"Received code generation request: {request}")
        
        # Zoek relevante code herinneringen
        relevant_memories = await knowledge_cluster.retrieve_knowledge(
            query=f"Code generatie voor {request.language}: {request.prompt}",
            max_results=3,
            category='code'
        )
        logger.debug(f"Relevant code memories: {relevant_memories}")
        
        # Bereid context voor met code herinneringen
        enhanced_context = "\n\n".join([
            f"Relevante code herinnering: {memory.metadata.get('content', '')}" 
            for memory in relevant_memories
        ]) + f"\n\nGeneratie opdracht: {request.prompt}"
        logger.debug(f"Enhanced code context: {enhanced_context}")
        
        response = client.messages.create(
            model=MODELS["claude-3-opus"],
            max_tokens=1000,
            messages=[
                {"role": "user", "content": enhanced_context}
            ]
        )
        logger.debug(f"API Response: {response.content[0].text}")
        
        # Sla nieuwe code kennis op
        await knowledge_cluster.store_knowledge(
            content=response.content[0].text,
            category='code',
            importance=0.7
        )
        
        logger.debug("Code generation processed successfully")
        return {
            "code": response.content[0].text,
            "memories": [memory.metadata for memory in relevant_memories]
        }
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# Proces bericht met geavanceerde context
@app.post("/process_message")
async def process_message(request: MessageRequest):
    try:
        logger.debug(f"Received message request: {request}")

        # API key verificatie
        api_key = request.apiKey or os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            logger.error("No API key provided")
            raise HTTPException(status_code=401, detail="No API key provided")

        client = anthropic.Anthropic(api_key=api_key)
        
        # Initialiseer MCPManager met KnowledgeCluster
        mcp_manager = MCPManager(knowledge_cluster)
        enhanced_context = await mcp_manager.retrieve_context(request.message)
        logger.debug(f"Enhanced context from MCPManager: {enhanced_context}")
        
        # Voeg originele bericht toe aan de context
        enhanced_context += f"\n\nOorspronkelijke bericht: {request.message}"
        
        # Get model string
        model_version = MODELS.get(request.model)
        if not model_version:
            raise HTTPException(status_code=400, detail=f"Invalid model: {request.model}")
        
        response = client.messages.create(
            model=model_version,
            max_tokens=1000,
            messages=[
                {"role": "user", "content": enhanced_context}
            ]
        )
        logger.debug(f"API Response: {response.content[0].text}")
        
        # Sla nieuwe kennis op
        await knowledge_cluster.store_knowledge(
            content=response.content[0].text,
            category='message_response',
            importance=0.5
        )
        
        logger.debug("Message processed successfully")
        
        relevant_memories = await knowledge_cluster.retrieve_knowledge(request.message, 3)
        logger.debug(f"Relevant memories: {relevant_memories}")
        
        return {
            "content": response.content[0].text,
            "memories": [memory.metadata for memory in relevant_memories]
        }
    except anthropic.APIError as e:
        logger.error(f"Anthropic API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Anthropic API Error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# Nieuwe endpoint voor handmatig geheugen beheer
@app.post("/manage-memory")
async def manage_memory(request: MemoryManagementRequest):
    try:
        result = await knowledge_cluster.update_knowledge_importance(
            entry_id=request.entry_id,
            new_importance=request.importance,
            memory_type=request.memory_type
        )
        
        if result:
            return {"status": "success", "message": "Memory updated successfully"}
        else:
            raise HTTPException(status_code=400, detail="Memory update failed")
    except Exception as e:
        logger.error(f"Memory management error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Health Check met geheugen status
@app.get("/health")
async def health_check():
    try:
        # Voer een kleine geheugen cleanup uit
        await knowledge_cluster.cleanup_memories()
        
        logger.debug("Health check with memory cleanup completed")
        return {
            "status": "healthy", 
            "memory_layers": {
                "short_term": "active",
                "long_term": "active",
                "context": "active"
            }
        }
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
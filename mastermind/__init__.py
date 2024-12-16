"""MasterMind - Advanced multi-agent system leveraging different LLM models."""

# Core system imports
from mastermind.core import (
    Orchestrator,
    WorkerAgent,
    StrategistAgent,
    TaskResult,
    ModelType,
    Agent,
    ResponseBlock,
    ToolUseBlock,
    format_block,
    is_response_block
)

# MCP protocol imports
from mastermind.mcp import (
    MCPManager,
    MCPProvider,
    MCPResource,
    MCPTool,
    MCPEnabledAgent,
    FileSystemProvider
)

# Database and memory management
from mastermind.database_protocol import DatabaseEntry
from mastermind.database import Memory
from mastermind.vectordb import VectorDatabase, VectorEntry
from mastermind.knowledge_cluster import KnowledgeCluster

# Server componenten toevoegen
from mastermind.server import (
    ChatRequest,
    CodeGenerationRequest,
    MessageRequest,
    MemoryManagementRequest
)

__version__ = '0.2.0'

__all__ = [
    # Core system components
    'Orchestrator',
    'WorkerAgent',
    'StrategistAgent',
    'TaskResult',
    'ModelType',
    'Agent',
    'ResponseBlock',
    'ToolUseBlock',
    'format_block',
    'is_response_block',
    
    # MCP protocol components
    'MCPManager',
    'MCPProvider',
    'MCPResource',
    'MCPTool',
    'MCPEnabledAgent',
    'FileSystemProvider',
    
    # Database components
    'DatabaseEntry',
    'Memory',
    
    # Memory management components
    'VectorDatabase',
    'VectorEntry',
    'KnowledgeCluster',
    
    # Server componenten toevoegen
    'app',
    'ChatRequest',
    'CodeGenerationRequest',
    'MessageRequest',
    'MemoryManagementRequest',
]
"""MasterMind - Advanced multi-agent system leveraging different LLM models."""

# Core system imports
from mastermind.core import (
    Orchestrator,
    WorkerAgent,
    StrategistAgent,
    TaskResult,
    ModelType,
    Agent
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

__version__ = '0.1.2'

__all__ = [
    # Core system components
    'Orchestrator',
    'WorkerAgent',
    'StrategistAgent',
    'TaskResult',
    'ModelType',
    'Agent',
    
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
    'KnowledgeCluster'
]
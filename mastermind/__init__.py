"""MasterMind - Advanced multi-agent system leveraging different LLM models."""

from mastermind.core import (
    Orchestrator,
    WorkerAgent,
    StrategistAgent,
    TaskResult,
    ModelType,
    Agent
)

from mastermind.mcp import (
    MCPManager,
    MCPProvider,
    MCPResource,
    MCPTool,
    MCPEnabledAgent,
    FileSystemProvider
)

from mastermind.vectordb import (
    VectorDatabase,
    VectorEntry
)

__version__ = '0.1.0'

__all__ = [
    # Core components
    'Orchestrator',
    'WorkerAgent',
    'StrategistAgent',
    'TaskResult',
    'ModelType',
    'Agent',
    
    # MCP components
    'MCPManager',
    'MCPProvider',
    'MCPResource',
    'MCPTool',
    'MCPEnabledAgent',
    'FileSystemProvider',
    
    # Vector database components
    'VectorDatabase',
    'VectorEntry'
]
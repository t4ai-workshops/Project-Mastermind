from typing import Dict, List, Any, Optional, Callable, TypeVar, Protocol, Union, Awaitable, Generic
from dataclasses import dataclass
import asyncio
from abc import ABC, abstractmethod
from mastermind.knowledge_cluster import KnowledgeCluster
from aiofiles import open as aio_open

T_co = TypeVar('T_co', covariant=True)  # Covariant type variable

class AsyncCallable(Protocol[T_co]):
    async def __call__(self, *args: Any, **kwargs: Any) -> T_co: ...

@dataclass
class MCPResource:
    """Represents a resource that can be exposed to LLMs"""
    name: str
    type: str
    content: Any
    metadata: Dict[str, Any]

@dataclass
class MCPTool:
    """Represents a tool that LLMs can use"""
    name: str
    description: str
    function: AsyncCallable[Any]
    parameters: Dict[str, Any]

class MCPProvider(ABC):
    """Base class for MCP resource and tool providers"""
    @abstractmethod
    async def get_resources(self) -> List[MCPResource]:
        """Get all available resources"""
        pass
    
    @abstractmethod
    async def get_tools(self) -> List[MCPTool]:
        """Get all available tools"""
        pass

class MCPManager:
    """Beheer van Multi-Context Processing (MCP)"""
    
    def __init__(self, knowledge_cluster: KnowledgeCluster):
        self.knowledge_cluster = knowledge_cluster
        self.resources: Dict[str, MCPResource] = {}
        self.tools: Dict[str, MCPTool] = {}
    
    async def register_tool(self, tool: MCPTool) -> None:
        """Registreer een nieuw hulpmiddel"""
        self.tools[tool.name] = tool
    
    async def use_tool(self, tool_name: str, *args: Any, **kwargs: Any) -> Any:
        """Gebruik een specifiek hulpmiddel binnen MCP"""
        if tool_name in self.tools:
            tool = self.tools[tool_name]
            return await tool.function(*args, **kwargs)
        raise ValueError(f"Hulpmiddel {tool_name} niet gevonden")

class FileSystemProvider(MCPProvider):
    """Provides file system access via MCP"""
    async def get_resources(self) -> List[MCPResource]:
        """Get file system resources"""
        return [
            MCPResource(
                name="project_files",
                type="directory",
                content="/path/to/project",
                metadata={"readable": True, "writable": True}
            )
        ]
    
    async def get_tools(self) -> List[MCPTool]:
        """Get file system tools"""
        return [
            MCPTool(
                name="read_file",
                description="Read contents of a file",
                function=self._read_file,
                parameters={"path": "str"}
            ),
            MCPTool(
                name="write_file",
                description="Write contents to a file",
                function=self._write_file,
                parameters={"path": "str", "content": "str"}
            )
        ]
    
    async def _read_file(self, path: str) -> str:
        """Read file contents"""
        async with aio_open(path, 'r') as f:
            content = await f.read()
            return str(content)
    
    async def _write_file(self, path: str, content: str) -> None:
        """Write file contents"""
        async with aio_open(path, 'w') as f:
            await f.write(content)

class MCPEnabledAgent:
    """Mixin to add MCP capabilities to agents"""
    def __init__(self, mcp_manager: MCPManager) -> None:
        self.mcp = mcp_manager
    
    async def get_context(self, query: str) -> List[MCPResource]:
        """Get relevant resources for a given query"""
        resources = []
        for resource in self.mcp.resources.values():
            if query.lower() in str(resource.content).lower():
                resources.append(resource)
        return resources
    
    async def use_tool(self, name: str, **kwargs: Any) -> Any:
        """Use an MCP tool"""
        return await self.mcp.use_tool(name, **kwargs)
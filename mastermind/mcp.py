from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import asyncio
from abc import ABC, abstractmethod

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
    function: callable
    parameters: Dict[str, Any]

class MCPProvider(ABC):
    """Base class for MCP resource and tool providers"""
    @abstractmethod
    async def get_resources(self) -> List[MCPResource]:
        pass
    
    @abstractmethod
    async def get_tools(self) -> List[MCPTool]:
        pass

class MCPManager:
    """Manages MCP resources and tools"""
    def __init__(self):
        self.providers: List[MCPProvider] = []
        self.resources: Dict[str, MCPResource] = {}
        self.tools: Dict[str, MCPTool] = {}
    
    def register_provider(self, provider: MCPProvider) -> None:
        """Register a new MCP provider"""
        self.providers.append(provider)
    
    async def initialize(self) -> None:
        """Initialize all resources and tools from providers"""
        for provider in self.providers:
            resources = await provider.get_resources()
            tools = await provider.get_tools()
            
            for resource in resources:
                self.resources[resource.name] = resource
            
            for tool in tools:
                self.tools[tool.name] = tool
    
    async def get_resource(self, name: str) -> Optional[MCPResource]:
        """Get a specific resource by name"""
        return self.resources.get(name)
    
    async def use_tool(self, name: str, **kwargs) -> Any:
        """Use a specific tool with given parameters"""
        tool = self.tools.get(name)
        if tool is None:
            raise ValueError(f"Tool {name} not found")
        return await tool.function(**kwargs)

class FileSystemProvider(MCPProvider):
    """Provides file system access via MCP"""
    async def get_resources(self) -> List[MCPResource]:
        # Example: expose specific directories as resources
        return [
            MCPResource(
                name="project_files",
                type="directory",
                content="/path/to/project",
                metadata={"readable": True, "writable": True}
            )
        ]
    
    async def get_tools(self) -> List[MCPTool]:
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
        with open(path, 'r') as f:
            return f.read()
    
    async def _write_file(self, path: str, content: str) -> None:
        with open(path, 'w') as f:
            f.write(content)

# Update the Agent class to use MCP
class MCPEnabledAgent:
    """Mixin to add MCP capabilities to agents"""
    def __init__(self, mcp_manager: MCPManager):
        self.mcp = mcp_manager
    
    async def get_context(self, query: str) -> List[MCPResource]:
        """Get relevant resources for a given query"""
        # In a real implementation, this would use semantic search
        return [
            resource for resource in self.mcp.resources.values()
            if query.lower() in str(resource.content).lower()
        ]
    
    async def use_tool(self, name: str, **kwargs) -> Any:
        """Use an MCP tool"""
        return await self.mcp.use_tool(name, **kwargs)

# Example integration with our existing Orchestrator
class EnhancedOrchestrator:
    def __init__(self, api_key: str):
        self.mcp_manager = MCPManager()
        self.mcp_manager.register_provider(FileSystemProvider())
        
    async def initialize(self):
        """Initialize MCP and other components"""
        await self.mcp_manager.initialize()
        
    async def process_task(self, task: str) -> Any:
        """Process a task with MCP capabilities"""
        # Get relevant context
        context = []
        for worker in self.workers:
            if isinstance(worker, MCPEnabledAgent):
                resources = await worker.get_context(task)
                context.extend(resources)
        
        # Enhanced processing with context
        strategy = await self.strategist.process({
            "task": task,
            "context": context
        })
        
        # ... rest of processing
from typing import Dict, List, Any, Optional, Callable, TypeVar, Protocol, Union
from dataclasses import dataclass
import asyncio
from abc import ABC, abstractmethod

T = TypeVar('T')

class AsyncCallable(Protocol):
    async def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

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
    function: Union[Callable[..., Any], AsyncCallable]
    parameters: Dict[str, Any]

# Rest of the file remains the same
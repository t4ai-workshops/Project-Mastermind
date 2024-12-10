from abc import ABC, abstractmethod
import asyncio
import logging
from typing import List, Dict, Any, Optional, cast, Awaitable
from dataclasses import dataclass
from enum import Enum
import anthropic
from anthropic.types import Message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelType(Enum):
    HAIKU = "claude-3-haiku"
    SONNET = "claude-3.5-sonnet"
    OPUS = "claude-3-opus"


@dataclass
class TaskResult:
    success: bool
    data: Any
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class Agent(ABC):
    def __init__(self, model_type: ModelType, client: anthropic.Client) -> None:
        self.model = model_type
        self.client = client
        self.context: Dict[str, Any] = {}
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @abstractmethod
    async def process(self, task: Any) -> TaskResult:
        pass

    async def think(self, prompt: str) -> str:
        try:
            self.logger.info(f"Agent {self.model.value} thinking about task")
            response = await cast(Awaitable[Any], self.client.messages.create(
                model=self.model.value,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            ))
            message = cast(Message, response)
            self.logger.debug(f"Received response from {self.model.value}")
            return str(message.content)
        except Exception as e:
            self.logger.error(f"Error in think method: {str(e)}")
            raise
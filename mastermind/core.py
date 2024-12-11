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
            if hasattr(response, 'content'):
                return str(response.content)
            return str(response)
        except Exception as e:
            self.logger.error(f"Error in think method: {str(e)}")
            raise


class WorkerAgent(Agent):
    """Haiku-based agent for quick processing tasks"""
    def __init__(self, client: anthropic.Client) -> None:
        super().__init__(ModelType.HAIKU, client)

    async def process(self, task: Any) -> TaskResult:
        try:
            self.logger.info("WorkerAgent processing task")
            result = await self.think(str(task))
            return TaskResult(success=True, data=result)
        except Exception as e:
            self.logger.error(f"Error in WorkerAgent: {str(e)}")
            return TaskResult(success=False, data=None, error=str(e))


class StrategistAgent(Agent):
    """Sonnet-based agent for complex reasoning"""
    def __init__(self, client: anthropic.Client) -> None:
        super().__init__(ModelType.SONNET, client)

    async def process(self, task: Any) -> TaskResult:
        try:
            self.logger.info("StrategistAgent analyzing task")
            prompt = f"""
            Task Analysis Required:
            {task}
            
            Please provide:
            1. Task decomposition
            2. Strategic approach
            3. Potential challenges
            4. Recommended solution path
            """
            result = await self.think(prompt)
            return TaskResult(success=True, data=result)
        except Exception as e:
            self.logger.error(f"Error in StrategistAgent: {str(e)}")
            return TaskResult(success=False, data=None, error=str(e))


class Orchestrator:
    def __init__(self, api_key: str) -> None:
        self.client = anthropic.Client(api_key=api_key)
        self.workers: List[WorkerAgent] = []
        self.strategist = StrategistAgent(self.client)
        self.logger = logging.getLogger(f"{__name__}.Orchestrator")

    def add_worker(self) -> None:
        worker = WorkerAgent(self.client)
        self.workers.append(worker)
        self.logger.info(f"Added new worker (total workers: {len(self.workers)})")

    async def process_task(self, task: Any) -> TaskResult:
        self.logger.info("Starting task processing")

        # First, get strategic analysis
        self.logger.debug("Getting strategic analysis")
        strategy = await self.strategist.process(task)
        if not strategy.success:
            self.logger.error(f"Strategic analysis failed: {strategy.error}")
            return strategy

        # Distribute subtasks to workers
        self.logger.debug("Distributing tasks to workers")
        worker_tasks = []
        for i, worker in enumerate(self.workers):
            self.logger.debug(f"Assigning task to worker {i+1}")
            worker_tasks.append(worker.process(strategy.data))

        # Gather results
        self.logger.debug("Gathering worker results")
        results = await asyncio.gather(*worker_tasks, return_exceptions=True)

        # Combine and analyze results
        self.logger.debug("Performing final analysis")
        final_analysis = await self.strategist.process({
            "original_task": task,
            "strategy": strategy.data,
            "worker_results": results
        })

        self.logger.info("Task processing completed")
        return final_analysis
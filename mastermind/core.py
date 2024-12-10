from abc import ABC, abstractmethod
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import anthropic

class ModelType(Enum):
    HAIKU = "claude-3-haiku"
    SONNET = "claude-3.5-sonnet"
    OPUS = "claude-3-opus"

@dataclass
class TaskResult:
    success: bool
    data: Any
    error: Optional[str] = None
    metadata: Optional[Dict] = None

class Agent(ABC):
    def __init__(self, model_type: ModelType, client: anthropic.Client):
        self.model = model_type
        self.client = client
        self.context = {}
    
    @abstractmethod
    async def process(self, task: Any) -> TaskResult:
        pass
    
    async def think(self, prompt: str) -> str:
        message = await self.client.messages.create(
            model=self.model.value,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content

class WorkerAgent(Agent):
    """Haiku-based agent for quick processing tasks"""
    def __init__(self, client: anthropic.Client):
        super().__init__(ModelType.HAIKU, client)
    
    async def process(self, task: Any) -> TaskResult:
        try:
            result = await self.think(str(task))
            return TaskResult(success=True, data=result)
        except Exception as e:
            return TaskResult(success=False, data=None, error=str(e))

class StrategistAgent(Agent):
    """Sonnet-based agent for complex reasoning"""
    def __init__(self, client: anthropic.Client):
        super().__init__(ModelType.SONNET, client)
    
    async def process(self, task: Any) -> TaskResult:
        try:
            # Enhanced prompt for strategic thinking
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
            return TaskResult(success=False, data=None, error=str(e))

class Orchestrator:
    def __init__(self, api_key: str):
        self.client = anthropic.Client(api_key=api_key)
        self.workers: List[WorkerAgent] = []
        self.strategist = StrategistAgent(self.client)
    
    def add_worker(self) -> None:
        self.workers.append(WorkerAgent(self.client))
    
    async def process_task(self, task: Any) -> TaskResult:
        # First, get strategic analysis
        strategy = await self.strategist.process(task)
        if not strategy.success:
            return strategy
        
        # Distribute subtasks to workers
        worker_tasks = []
        for worker in self.workers:
            worker_tasks.append(worker.process(strategy.data))
        
        # Gather results
        results = await asyncio.gather(*worker_tasks, return_exceptions=True)
        
        # Combine and analyze results
        final_analysis = await self.strategist.process({
            "original_task": task,
            "strategy": strategy.data,
            "worker_results": results
        })
        
        return final_analysis
import pytest
from unittest.mock import AsyncMock, MagicMock
from mastermind.core import ModelType, TaskResult, WorkerAgent, StrategistAgent
from anthropic.types import Message, MessageParam, TextBlock


def test_model_types():
    assert ModelType.HAIKU.value == "claude-3-haiku"
    assert ModelType.SONNET.value == "claude-3.5-sonnet"
    assert ModelType.OPUS.value == "claude-3-opus"


def test_task_result():
    result = TaskResult(success=True, data="test")
    assert result.success
    assert result.data == "test"
    assert result.error is None
    assert result.metadata is None


@pytest.mark.asyncio
async def test_worker_agent():
    # Mock setup
    text_block = MagicMock(spec=TextBlock)  # Simuleert een TextBlock object
    text_block.text = "test response"       # Stelt de verwachte waarde in

    mock_message = MagicMock(spec=Message) # Simuleert een Message object
    mock_message.content = [text_block]    # Stel content in als een lijst van TextBlock objecten

    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_message  # Mock voor messages.create

    # Test
    agent = WorkerAgent(mock_client)
    result = await agent.process("test task")

    # Assertions
    assert result.success
    assert result.data == "test response"
    
@pytest.mark.asyncio
async def test_strategist_agent():
    # Create a mock client
    mock_client = AsyncMock()

    # Create a mock for the `think` method's return value
    mock_think_result = "1. Decompose task\n2. Strategy details\n3. Challenges\n4. Solution path"

    # Mock the `think` method of the agent
    StrategistAgent.think = AsyncMock(return_value=mock_think_result)

    # Instantiate the StrategistAgent with the mock client
    agent = StrategistAgent(mock_client)

    # Execute the agent's `process` method with a test task
    result = await agent.process("test task")

    # Assertions
    assert result.success, f"Expected success but got error: {result.error}"
    assert result.data == mock_think_result, f"Expected data to be '{mock_think_result}' but got {result.data}"

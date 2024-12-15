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
    mock_client = AsyncMock()
    mock_response = AsyncMock()
    mock_response.content = [MagicMock(text="strategy response")]
    mock_client.messages.create.return_value = mock_response
    
    agent = StrategistAgent(mock_client)
    result = await agent.process("test task")
    
    assert result.success
    assert result.data == "strategy response"
    mock_client.messages.create.assert_called_once()
    call_args = mock_client.messages.create.call_args[1]
    assert call_args['model'] == ModelType.SONNET.value

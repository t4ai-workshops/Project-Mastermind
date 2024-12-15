import pytest
from unittest.mock import AsyncMock, MagicMock
from mastermind.core import ModelType, TaskResult, WorkerAgent, StrategistAgent
from anthropic.types import Message, TextBlock


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
    text_block = MagicMock(spec=TextBlock)
    text_block.text = "test response"
    
    mock_message = MagicMock(spec=Message)
    mock_message.content = [text_block]
    
    mock_client = MagicMock()
    mock_client.messages = MagicMock()
    mock_client.messages.create = AsyncMock(return_value=mock_message)
    
    # Test
    agent = WorkerAgent(mock_client)
    result = await agent.process("test task")
    
    # Assertions
    assert result.success
    assert result.data == "test response"
    mock_client.messages.create.assert_called_once()
    call_args = mock_client.messages.create.call_args[1]
    assert call_args['model'] == ModelType.HAIKU.value
    assert call_args['max_tokens'] == 1024
    assert call_args['messages'][0]['content'] == "test task"


@pytest.mark.asyncio
async def test_strategist_agent():
    # Mock setup
    text_block = MagicMock(spec=TextBlock)
    text_block.text = "strategy response"
    
    mock_message = MagicMock(spec=Message)
    mock_message.content = [text_block]
    
    mock_client = MagicMock()
    mock_client.messages = MagicMock()
    mock_client.messages.create = AsyncMock(return_value=mock_message)
    
    # Test
    agent = StrategistAgent(mock_client)
    result = await agent.process("test task")
    
    # Assertions
    assert result.success
    assert result.data == "strategy response"
    mock_client.messages.create.assert_called_once()
    call_args = mock_client.messages.create.call_args[1]
    assert call_args['model'] == ModelType.SONNET.value

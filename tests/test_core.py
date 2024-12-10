import pytest
from unittest.mock import AsyncMock, MagicMock
from mastermind.core import ModelType, TaskResult, WorkerAgent, StrategistAgent


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
    # Create a proper async mock for the client
    mock_client = MagicMock()
    mock_client.messages = MagicMock()
    
    # The create method should be an AsyncMock with a proper return value structure
    mock_create = AsyncMock()
    mock_create.return_value.content = "test response"
    mock_client.messages.create = mock_create
    
    # Create agent with mock client
    agent = WorkerAgent(mock_client)
    
    # Test processing
    result = await agent.process("test task")
    assert result.success
    assert result.data == "test response"
    
    # Verify correct model was used
    mock_create.assert_called_once()
    call_args = mock_create.call_args[1]  # Get kwargs of the call
    assert call_args['model'] == ModelType.HAIKU.value
    assert call_args['max_tokens'] == 1024
    assert call_args['messages'][0]['content'] == "test task"


@pytest.mark.asyncio
async def test_strategist_agent():
    # Create a proper async mock for the client
    mock_client = MagicMock()
    mock_client.messages = MagicMock()
    
    # The create method should be an AsyncMock with a proper return value structure
    mock_create = AsyncMock()
    mock_create.return_value.content = "strategy response"
    mock_client.messages.create = mock_create
    
    # Create agent with mock client
    agent = StrategistAgent(mock_client)
    
    # Test processing
    result = await agent.process("test task")
    assert result.success
    assert result.data == "strategy response"
    
    # Verify correct model was used
    mock_create.assert_called_once()
    call_args = mock_create.call_args[1]  # Get kwargs of the call
    assert call_args['model'] == ModelType.SONNET.value

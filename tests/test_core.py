import pytest
from unittest.mock import AsyncMock as AsyncMockBase
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
async def test_worker_agent(mocker):
    # Create a mock messages object with async create method
    mock_messages = mocker.Mock()
    mock_messages.create = AsyncMockBase(return_value=mocker.Mock(content="test response"))
    
    # Create mock client with messages attribute
    mock_client = mocker.Mock()
    mock_client.messages = mock_messages
    
    # Create agent with mock client
    agent = WorkerAgent(mock_client)
    
    # Test processing
    result = await agent.process("test task")
    assert result.success
    assert result.data == "test response"
    
    # Verify the mock was called correctly
    mock_messages.create.assert_called_once_with(
        model="claude-3-haiku",
        max_tokens=1024,
        messages=[{"role": "user", "content": "test task"}]
    )

@pytest.mark.asyncio
async def test_strategist_agent(mocker):
    # Create a mock messages object with async create method
    mock_messages = mocker.Mock()
    mock_messages.create = AsyncMockBase(return_value=mocker.Mock(content="strategy response"))
    
    # Create mock client with messages attribute
    mock_client = mocker.Mock()
    mock_client.messages = mock_messages
    
    # Create agent with mock client
    agent = StrategistAgent(mock_client)
    
    # Test processing
    result = await agent.process("test task")
    assert result.success
    assert result.data == "strategy response"
    
    # Verify the mock was called with correct model
    mock_messages.create.assert_called_once()
    assert mock_messages.create.call_args[1]["model"] == "claude-3.5-sonnet"
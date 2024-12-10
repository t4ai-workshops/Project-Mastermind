import pytest
from unittest.mock import AsyncMock
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
    # Create mock response with async create method
    mock_response = mocker.Mock()
    mock_response.content = "test response"

    # Create messages mock
    mock_messages = mocker.Mock()
    mock_messages.create = AsyncMock(return_value=mock_response)

    # Create client mock
    mock_client = mocker.Mock()
    mock_client.messages = mock_messages

    # Create agent with mock client
    agent = WorkerAgent(mock_client)

    # Test processing
    result = await agent.process("test task")
    assert result.success
    assert result.data == "test response"


@pytest.mark.asyncio
async def test_strategist_agent(mocker):
    # Create mock response with async create method
    mock_response = mocker.Mock()
    mock_response.content = "strategy response"

    # Create messages mock
    mock_messages = mocker.Mock()
    mock_messages.create = AsyncMock(return_value=mock_response)

    # Create client mock
    mock_client = mocker.Mock()
    mock_client.messages = mock_messages

    # Create agent with mock client
    agent = StrategistAgent(mock_client)

    # Test processing
    result = await agent.process("test task")
    assert result.success
    assert result.data == "strategy response"

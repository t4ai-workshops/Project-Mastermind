# Testing Strategy for Claude 3 API Integration

## Key Principles

1. Direct Message Object Mocking
```python
# Correct mock structure for Claude 3 API responses:
text_block = MagicMock(spec=TextBlock)  
text_block.text = "expected response"       
mock_message = MagicMock(spec=Message) 
mock_message.content = [text_block]    
mock_client.messages.create.return_value = mock_message
```

2. Method Level Mocking (Alternative Approach)
```python
# For complex scenarios, mock the think method directly:
mock_result = "expected structured response"
StrategistAgent.think = AsyncMock(return_value=mock_result)
```

## Important Notes:
- Claude 3 API doesn't require awaiting messages.create()
- TextBlock must be properly structured in content list
- Use proper type specs (Message, TextBlock) for accurate mocking
- Maintain async context for process() method tests

## Testing Patterns:

1. Basic Response Testing:
```python
@pytest.mark.asyncio
async def test_agent():
    # Setup message structure
    text_block = MagicMock(spec=TextBlock)
    text_block.text = "response"
    mock_message = MagicMock(spec=Message)
    mock_message.content = [text_block]
    
    # Setup client
    mock_client = MagicMock()
    mock_client.messages.create.return_value = mock_message
    
    # Test & Assert
    agent = Agent(mock_client)
    result = await agent.process("task")
    assert result.success
    assert result.data == "response"
```

2. Complex Response Testing:
```python
@pytest.mark.asyncio
async def test_complex_agent():
    # Mock think method directly
    mock_result = "structured response"
    Agent.think = AsyncMock(return_value=mock_result)
    
    # Test & Assert
    agent = Agent(AsyncMock())
    result = await agent.process("task")
    assert result.success
    assert result.data == mock_result
```
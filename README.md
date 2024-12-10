# Project Master Mind

An advanced multi-agent system leveraging different LLM models (Claude 3 family) for enhanced cognitive capabilities.

## Overview

Project Master Mind is an experimental framework that combines different Large Language Models (LLMs) into a coordinated system with enhanced reasoning capabilities. It uses:

- Claude 3 Haiku for quick, efficient processing tasks
- Claude 3.5 Sonnet for complex reasoning and orchestration
- Claude 3 Opus for specialized deep analysis

## Architecture

The system consists of several key components:

1. **Agents**
   - WorkerAgent (Haiku-based) for quick processing
   - StrategistAgent (Sonnet-based) for complex reasoning
   - Specialized agents can be added as needed

2. **Orchestrator**
   - Coordinates multiple agents
   - Manages task distribution
   - Handles result aggregation

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
import asyncio
from mastermind.core import Orchestrator

async def main():
    orchestrator = Orchestrator("your-api-key")
    orchestrator.add_worker()
    
    result = await orchestrator.process_task(
        "Your complex task here"
    )
    print(result.data)

if __name__ == "__main__":
    asyncio.run(main())
```

## Future Development

- Memory system for context retention
- Enhanced inter-agent communication
- Metrics and monitoring
- Integration with Claude 3 Opus for specialized tasks

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
# Project MasterMind

An advanced multi-agent system leveraging different LLM models (Claude 3 family) for enhanced cognitive capabilities.

## Overview

Project MasterMind combines different Large Language Models (LLMs) into a coordinated system with enhanced reasoning capabilities. It uses:

- Claude 3 Haiku for quick, efficient processing tasks
- Claude 3.5 Sonnet for complex reasoning and orchestration
- Claude 3 Opus for specialized deep analysis

## Prerequisites

- Python 3.8 or higher
- An Anthropic API key (Claude access)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/t4ai-workshops/Project-Mastermind.git
cd Project-Mastermind
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your API key:

You'll need an Anthropic API key to use this project. There are two ways to provide it:

A. Using a .env file (recommended for local development):
```bash
# Create a .env file in the project root
echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
```

B. Setting an environment variable:
```bash
# Linux/Mac
export ANTHROPIC_API_KEY=your-api-key-here

# Windows
set ANTHROPIC_API_KEY=your-api-key-here
```

⚠️ **Important**: Never commit your API key to version control!

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

## Contributing

We welcome contributions! To contribute:

1. Fork the repository
2. Create your feature branch
3. Setup your development environment:
   - Install development dependencies: `pip install -r requirements.txt`
   - Configure your Anthropic API key as described above
   - Run tests to verify your setup: `pytest tests/`
4. Commit your changes
5. Push to your branch
6. Create a Pull Request

Note: When running tests locally or in your own fork's CI/CD pipeline, you'll need to use your own Anthropic API key. The project's CI/CD uses a separate key that is only available for the main repository's workflow.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## License

MIT

## Support

For questions or discussions, please open an issue in the repository.
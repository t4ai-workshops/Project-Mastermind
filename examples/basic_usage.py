import asyncio
import logging
from mastermind.core import Orchestrator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def main():
    # Initialize the orchestrator with your API key
    orchestrator = Orchestrator("your-api-key")
    
    # Add two worker agents
    orchestrator.add_worker()
    orchestrator.add_worker()
    
    # Define a complex task
    task = """
    Analyze the potential impact of quantum computing on current encryption methods.
    Consider both immediate and long-term implications for:
    1. Current RSA encryption
    2. Post-quantum cryptography
    3. Financial system security
    """
    
    # Process the task and get results
    result = await orchestrator.process_task(task)
    
    # Print the results
    if result.success:
        print("\nTask Analysis Results:")
        print("-" * 50)
        print(result.data)
    else:
        print(f"\nError during analysis: {result.error}")

if __name__ == "__main__":
    asyncio.run(main())
# Contributing to Project MasterMind

We love your input! We want to make contributing to Project MasterMind as easy and transparent as possible.

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/Project-Mastermind.git`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your API key:
   - You need your own Anthropic API key for development and testing
   - Create a .env file in the project root:
     ```bash
     echo "ANTHROPIC_API_KEY=your-api-key-here" > .env
     ```
   - ⚠️ Never commit this file to git!
   - The .env file is already in .gitignore

5. Verify your setup:
   ```bash
   pytest tests/
   ```

## API Key Usage

- Each developer needs their own Anthropic API key
- Your key is used only in your local environment and your fork
- The main repository's CI/CD uses a separate key
- Contributors never have access to the main repository's key
- When submitting PRs, tests will run using the main repository's key

## Development Process

1. Create a new branch: `git checkout -b feature-name`
2. Make your changes
3. Run tests locally (using your API key)
4. Commit your changes
5. Push to your fork
6. Create a Pull Request

## Writing Tests

- All new features should include tests
- Run tests locally before submitting PR: `pytest tests/`
- Tests should work with CI/CD environment
- Include proper error handling for API-related functions

## Pull Request Process

1. Update documentation if needed
2. Update the README.md if needed
3. The PR must pass all tests
4. Get approval from at least one maintainer

## License
By contributing, you agree that your contributions will be licensed under the MIT License.
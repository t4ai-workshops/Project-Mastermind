# MasterMind Desktop

Native desktop application for the MasterMind AI system, optimized for macOS and Apple Silicon.

## Prerequisites

Install using HomeBrew:

```bash
# Update HomeBrew
brew update

# Install Node.js
brew install node

# Install Rust
brew install rust

# Install system dependencies for Tauri
brew install gtk+3 webkit2gtk-4.0 libappindicator3 librsvg
```

## Development Setup

1. Install dependencies:
```bash
# Install project dependencies
npm install

# Install Tauri CLI
cargo install tauri-cli

# Verify Tauri installation
cargo tauri --version
```

2. Running in development mode:
```bash
# Start the development server
npm run tauri dev
```

3. Building for production:
```bash
# Create production build
npm run tauri build
```

The built application will be available in `src-tauri/target/release/bundle/`.

## Development Tools

Recommended tools for development:
- VSCode with Rust and React extensions
- Xcode Command Line Tools (will be prompted to install if needed)
- HomeBrew (for easy dependency management)

## Architecture

The application consists of:
- React + Tailwind frontend (in `src/`)
- Rust-based Tauri backend (in `src-tauri/`)
- Native system integration via Tauri
- Memory management system

## Contributing

See the main project [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## Running Tests

```bash
# Frontend tests
npm test

# Rust tests
cargo test
```

## Troubleshooting

Common issues:

1. Missing Xcode Command Line Tools:
```bash
xcode-select --install
```

2. HomeBrew installation:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

3. Node version issues:
```bash
# Install nvm for Node version management
brew install nvm
# Install and use specific Node version
nvm install 18
nvm use 18
```
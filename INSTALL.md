# Installation Guide for MasterMind

This guide will help you set up MasterMind on your macOS system, specifically optimized for Apple Silicon (M1/M2) Macs.

## Prerequisites

1. Install Homebrew if you haven't already:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install Rust:
```bash
brew install rust
```

3. Install Node.js:
```bash
brew install node
```

## Development Dependencies

1. Install development tools:
```bash
# Xcode Command Line Tools (if not already installed)
xcode-select --install

# Install additional dependencies
brew install pkg-config
```

## Building the Application

1. Clone the repository:
```bash
git clone https://github.com/t4ai-workshops/Project-Mastermind.git
cd Project-Mastermind
```

2. Install npm dependencies:
```bash
cd gui
npm install
```

3. Install Tauri CLI:
```bash
cargo install tauri-cli
```

## Running in Development Mode

```bash
npm run tauri dev
```

## Building for Production

```bash
npm run tauri build
```

The built application will be available in `src-tauri/target/release/bundle/`.

## Troubleshooting

### Common Issues

1. If you get node-gyp errors:
```bash
brew reinstall node
```

2. If Rust toolchain is not found:
```bash
rustup update
```

3. If you get permissions errors:
```bash
sudo chown -R $(whoami) $(npm config get prefix)/{lib/node_modules,bin,share}
```

### Updating Dependencies

To keep all dependencies up to date:
```bash
brew update && brew upgrade
rustup update
npm update
```

## Note on System Requirements

- macOS 11 Big Sur or later
- Apple Silicon (M1/M2) or Intel processor
- At least 4GB of RAM
- 1GB of free disk space

## Support

If you encounter any issues:
1. Check the [GitHub Issues](https://github.com/t4ai-workshops/Project-Mastermind/issues)
2. Submit a new issue if your problem hasn't been reported

## Additional Tips

1. For better development experience, recommended VSCode extensions:
   - Rust Analyzer
   - Tauri
   - React Developer Tools

2. For M1/M2 Macs, all dependencies are automatically compiled for ARM architecture when installed through Homebrew.

3. The app uses native system features for optimal performance on Apple Silicon.
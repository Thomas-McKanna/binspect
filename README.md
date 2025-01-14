# 🔍 Binspect - Secure Your Pipe-to-Shell Installations

[![PyPI version](https://badge.fury.io/py/binspect.svg)](https://badge.fury.io/py/binspect)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Binspect is a security tool that analyzes shell scripts before they're executed on your system. It's designed to make pipe-to-shell installations safer by detecting potentially malicious code.

## 🎬 See It In Action

![Demo](demo.gif)

## 🚨 The Problem

We've all seen installation instructions like this:

```bash
curl -fsSL https://example.com/install.sh | bash
```

This pattern is convenient but dangerous - you're executing code without reviewing it. Binspect helps bridge the security gap by analyzing scripts for malicious content before execution.

## ✨ Features

- 🤖 Uses AI to analyze shell scripts for malicious patterns
- 🔄 Works with a wide variety of LLM providers (uses LiteLLM to achieve this)
- 🎨 Rich terminal output with syntax highlighting
- 🛑 Interactive prompt to proceed or abort installation
- 🚀 Fast and efficient analysis
- 👁️ Less than 200 lines of Python - easily audit it yourself

## 🚀 Quick Start

Install using pip:

```bash
pip install binspect
```

Or with pipx:

```bash
pipx install binspect
```

## 📖 Usage

Instead of piping directly to bash, pipe through binspect first:

```bash
curl -fsSL https://example.com/install.sh | binspect | bash
```

Binspect will:

1. Analyze the script for suspicious patterns
2. Show you detailed findings
3. Ask for confirmation before proceeding
4. Pass the script to bash only if you approve

## ⚙️ Configuration

### LLM Provider Setup

Binspect uses LiteLLM under the hood, allowing you to use various LLM providers. Set up
your preferred provider using environment variables:

```bash
# For OpenAI
export OPENAI_API_KEY='your-api-key'

# For Anthropic/Claude
export ANTHROPIC_API_KEY='your-api-key'

# For other providers, see LiteLLM documentation
```

### Model Selection

Choose your preferred model using the `BASH_INSPECTOR_MODEL` environment variable:

```bash
# Default is 'openai/gpt-4o'
export BASH_INSPECTOR_MODEL='anthropic/claude-3-sonnet-20240229'
```

For a full list of providers, see https://docs.litellm.ai/docs/providers.

## 🔒 Security Notes

- Binspect is a helper tool, not a guarantee of safety
- Always review scripts manually when possible
- Use trusted sources and verify checksums
- Consider using package managers instead of pipe-to-shell when available

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

Binspect is provided as-is without any guarantees. While it can help identify obvious malicious patterns, it should not be your only security measure. Always exercise caution when executing scripts from the internet.

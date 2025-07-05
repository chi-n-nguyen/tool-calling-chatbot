# 🤖 AI Tool Calling Chatbot

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI GPT-4o-mini](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modular command-line AI assistant that integrates with OpenAI's GPT-4o-mini model, featuring an extensible tool system for function calling.

## 🎬 Demo

> **Note**: Add a demo GIF or video here to showcase the chatbot in action!

```bash
# Example interaction
$ chatbot

🤖 AI Tool Calling Chatbot

You: Calculate the area of a circle with radius 5
🔧 Tool Call: calculator(expression=3.14159 * 5 * 5)
✅ Result: 78.54
🤖 Assistant: The area of a circle with radius 5 is approximately 78.54 square units.

You: Tell me a programming joke
🔧 Tool Call: random_joke(category=programming)
✅ Result: Why do programmers prefer dark mode? Because light attracts bugs! 😄
🤖 Assistant: Here's a programming joke for you: Why do programmers prefer dark mode? Because light attracts bugs! 😄
```

## ✨ Features

- **🔧 Function Calling**: AI can automatically call predefined tools based on user requests
- **📊 Calculator**: Safe mathematical expression evaluation with AST parsing
- **📁 File Reader**: Read text files with comprehensive safety checks
- **😄 Random Jokes**: Get programming and general jokes for entertainment
- **🎨 Rich CLI**: Beautiful terminal interface with colors, animations, and formatting
- **🔄 Async Support**: Efficient asynchronous operations with concurrent tool execution
- **📝 Conversation History**: Maintain chat context across interactions with persistent memory
- **🛡️ Type Safety**: Comprehensive type hints throughout the codebase using modern Python typing
- **🔐 Security**: Input validation, safe code execution, and error handling

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.11 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- [uv](https://docs.astral.sh/uv/) for package management

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/chi-n-nguyen/tool-calling-chatbot.git
cd tool-calling-chatbot

# Install dependencies using uv
uv sync

# Install the package in development mode
uv pip install -e .
```

### 3. Configuration

Create a `.env` file in the project root:

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your API key
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Get Your OpenAI API Key

1. Visit [OpenAI's API Keys page](https://platform.openai.com/api-keys)
2. Sign up or log in to your account
3. Click "Create new secret key"
4. Copy the key and paste it into your `.env` file
5. **Important**: Add some credits to your OpenAI account to use the API

### 5. Run the Chatbot

```bash
# Method 1: Using the installed command
chatbot

# Method 2: Using Python directly  
python -m tool_calling_chatbot.main

# Method 3: For development
uv run python -m tool_calling_chatbot.main
```

## 🎯 Usage Examples

### Calculator Tool
```
You: Calculate 2 + 3 * 4
🤖 Assistant: I'll calculate that for you.
🔧 Tool Call: calculator(expression=2 + 3 * 4)
✅ Result: {'expression': '2 + 3 * 4', 'result': 14, 'formatted': '2 + 3 * 4 = 14'}
The result is 14.
```

### File Reader Tool
```
You: Read the content of README.md
🤖 Assistant: I'll read the README.md file for you.
🔧 Tool Call: file_reader(file_path=README.md)
✅ Result: {'file_path': '/path/to/README.md', 'content': '# Project Title...', 'lines_read': 45, 'truncated': False}
Here's the content of README.md: [content shown]
```

### Random Joke Tool
```
You: Tell me a programming joke
🤖 Assistant: Here's a programming joke for you!
🔧 Tool Call: random_joke(category=programming)
✅ Result: {'setup': 'Why do programmers prefer dark mode?', 'punchline': 'Because light attracts bugs!', 'category': 'programming'}
Why do programmers prefer dark mode? Because light attracts bugs! 😄
```

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `/help` | Show help message |
| `/tools` | List available tools |
| `/history` | Show conversation history |
| `/clear` | Clear conversation history |
| `/exit` or `/quit` | Exit the chatbot |

## 🔧 Available Tools

### Calculator
- **Function**: `calculator`
- **Description**: Evaluates mathematical expressions safely
- **Parameters**: `expression` (string) - Mathematical expression to evaluate
- **Example**: `"2 + 3 * 4"`, `"pow(2, 3)"`, `"abs(-5)"`

### File Reader
- **Function**: `file_reader`
- **Description**: Reads text files safely with size and type restrictions
- **Parameters**: 
  - `file_path` (string, required) - Path to the file
  - `max_lines` (integer, optional) - Maximum lines to read (default: 100)
- **Supported formats**: `.txt`, `.md`, `.py`, `.js`, `.html`, `.css`, `.json`, `.yaml`, `.yml`, `.xml`

### Random Joke
- **Function**: `random_joke`
- **Description**: Provides random jokes for entertainment
- **Parameters**: `category` (string, optional) - Category of joke ("programming", "general", "any")

## 🏗️ Project Structure

```
tool-calling-chatbot/
├── src/
│   └── tool_calling_chatbot/
│       ├── __init__.py
│       ├── main.py              # Main entry point
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py        # Configuration management
│       │   ├── base.py          # Base classes and registry
│       │   ├── openai_client.py # OpenAI integration
│       │   └── cli.py           # CLI interface
│       └── tools/
│           ├── __init__.py
│           ├── calculator.py    # Calculator tool
│           ├── file_reader.py   # File reader tool
│           └── random_joke.py   # Random joke tool
├── pyproject.toml              # Project configuration
├── .env.example               # Environment template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🛠️ Development Guide

### Adding New Tools

1. **Create a new tool file** in `src/tool_calling_chatbot/tools/`:

```python
from typing import Any, List
from ..core.base import BaseTool, ToolParameter, ToolResult

class YourTool(BaseTool):
    @property
    def name(self) -> str:
        return "your_tool"
    
    @property
    def description(self) -> str:
        return "Description of what your tool does"
    
    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="param_name",
                type="string",
                description="Parameter description",
                required=True
            )
        ]
    
    async def execute(self, param_name: str) -> ToolResult:
        # Your tool logic here
        return ToolResult(
            success=True,
            data={"result": "your_result"}
        )
```

2. **Register the tool** in `src/tool_calling_chatbot/tools/__init__.py`:

```python
from .your_tool import YourTool

your_tool = YourTool()
registry.register(your_tool)
```

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Yes | - |
| `OPENAI_MODEL` | OpenAI model to use | No | `gpt-4o-mini` |
| `OPENAI_TEMPERATURE` | Response randomness (0.0-2.0) | No | `0.7` |
| `OPENAI_MAX_TOKENS` | Maximum tokens per response | No | `1000` |

### Running Tests

```bash
# Run with pytest (when tests are added)
uv run pytest

# Run type checking
uv run mypy src/
```

## 🔒 Security Features

- **Safe Expression Evaluation**: Calculator uses AST parsing to prevent code injection
- **File Access Controls**: File reader has size limits and extension restrictions
- **Input Validation**: All tool parameters are validated before execution
- **Error Handling**: Comprehensive error handling prevents crashes

## 🐛 Troubleshooting

### Common Issues

1. **"OpenAI API key not found"**
   - Check that your `.env` file exists and contains `OPENAI_API_KEY`
   - Ensure the API key is valid and has credits

2. **"Tool not found" errors**
   - Verify all tools are properly registered in `tools/__init__.py`
   - Check for import errors in tool modules

3. **"File not found" when reading files**
   - Use absolute paths or ensure files exist relative to current directory
   - Check file permissions and supported extensions

### Debug Mode

Set environment variables for debugging:

```bash
export PYTHONPATH=src
export OPENAI_LOG_LEVEL=debug
```

## 📚 Learning Resources

- [OpenAI Function Calling Documentation](https://platform.openai.com/docs/guides/function-calling)
- [Rich Terminal Library](https://rich.readthedocs.io/)
- [Pydantic for Data Validation](https://pydantic-docs.helpmanual.io/)
- [Modern Python Typing](https://docs.python.org/3/library/typing.html)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes with proper type hints
4. Test your changes
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- OpenAI for the GPT-4o-mini model
- Rich library for beautiful terminal output
- Python community for excellent async support

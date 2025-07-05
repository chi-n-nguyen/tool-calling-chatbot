# Tool Calling Chatbot

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI GPT-4o-mini](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**For AI @ DSCubed Winter Program 2025**

A project I built to make my winter break meaningful - learning function calling with OpenAI while building tools around my actual interests (vintage fashion & food). Started as Project 1 requirements but evolved into something more personal.

Built a modular command-line AI assistant that integrates with OpenAI's GPT-4o-mini, featuring three distinct function calling patterns that showcase different use cases.

## Function Calling Patterns

This project demonstrates 3 different function calling approaches:

**Tool 1: Calculator**  
- Required by Project 1: Safe mathematical expression evaluation
- Pattern: Direct computation with validation and error handling
- Showcases: AST parsing, security considerations, structured output

**Tool 2: Vintage Outfit Generator** 
- Personal choice: My interest in fashion and Narrm's vintage scene  
- Pattern: Combinatorial generation with contextual logic
- Showcases: Random selection, seasonal adaptation, local knowledge integration

**Tool 3: Narrm Food Recommender** 
- Personal choice: Being a bit of a foodie in Melbourne
- Pattern: Filtering and recommendation with multi-criteria logic
- Showcases: Complex parameter handling, data filtering, personalized results

## Quick Demo

```bash
$ chatbot

AI Tool Calling Chatbot

You: Calculate the compound interest on $1000 at 5% for 3 years
Tool Call: calculator(expression=1000 * (1 + 0.05)**3)
Result: $1157.63

You: Generate a vintage outfit for a concert in winter
Tool Call: vintage_outfit_generator(occasion=concert, season=winter)
Result: Oversized band tee, vintage leather jacket, Doc Martens...

You: Recommend a cheap restaurant for students
Tool Call: narrm_food_recommender(budget=cheap, student=true)
Result: Dumplings Plus - handmade dumplings, $8-12, student discount available
```

## Features

- **Smart Function Calling** - AI automatically selects the right tool for your request
- **Security First** - Safe code execution with AST parsing for calculations
- **Local Knowledge** - Narrm-focused recommendations with real local spots
- **Rich CLI** - Beautiful terminal interface with proper styling
- **Async Operations** - Efficient concurrent tool execution
- **Type Safety** - Comprehensive type hints throughout
- **Conversation Memory** - Maintains context across interactions

## Setup

### Prerequisites
- Python 3.11+
- OpenAI API key ([grab one here](https://platform.openai.com/api-keys))
- [uv](https://docs.astral.sh/uv/) for package management

### Installation
```bash
git clone https://github.com/chi-n-nguyen/tool-calling-chatbot.git
cd tool-calling-chatbot

# Install dependencies
uv sync

# Install in development mode
uv pip install -e .
```

### Configuration
```bash
# Copy example environment file
cp .env.example .env

# Add your OpenAI API key
echo "OPENAI_API_KEY=your_key_here" >> .env
```

**Pro tip**: Add some credits to your OpenAI account before testing!

### Run It
```bash
# Simple way
chatbot

# Or directly
python -m tool_calling_chatbot.main

# Development mode
uv run python -m tool_calling_chatbot.main
```

## Usage Examples

### Calculator Tool
```
You: What's the area of a circle with radius 7?
Assistant: I'll calculate that for you.
Tool Call: calculator(expression=3.14159 * 7 * 7)
Result: 153.94 square units
```

### Vintage Outfit Generator
```
You: I need a vintage Narrm outfit for a date night in autumn
Assistant: Perfect! Let me create a vintage Narrm outfit for your autumn date.
Tool Call: vintage_outfit_generator(occasion=date, season=autumn)
Result: Vintage outfit with curated Narrm shopping spots and seasonal tips
```

### Narrm Food Recommender
```
You: Find me a good spot for lunch under $20
Assistant: I'll find you a great lunch spot within budget.
Tool Call: narrm_food_recommender(budget=moderate, cuisine=any)
Result: Pellegrini's Espresso Bar - authentic Italian since 1954, $6-15
```

## Available Tools

| Tool | Function | Purpose |
|------|----------|---------|
| Calculator | `calculator` | Mathematical expression evaluation |
| Vintage Generator | `vintage_outfit_generator` | Narrm-focused vintage outfit recommendations |
| Food Recommender | `narrm_food_recommender` | Local restaurant suggestions with student discounts |

## Project Structure

```
tool-calling-chatbot/
├── src/tool_calling_chatbot/
│   ├── core/
│   │   ├── config.py           # Environment configuration
│   │   ├── base.py             # Base classes and registry
│   │   ├── openai_client.py    # OpenAI integration
│   │   └── cli.py              # CLI interface
│   ├── tools/
│   │   ├── calculator.py       # Mathematical calculations
│   │   ├── vintage_outfit_generator.py  # Fashion recommendations
│   │   └── narrm_food_recommender.py   # Food recommendations
│   └── main.py                 # Entry point
├── pyproject.toml             # Project configuration
└── .env.example              # Environment template
```

## Adding New Tools

1. **Create Your Tool**
```python
from ..core.base import BaseTool, ToolParameter, ToolResult

class YourTool(BaseTool):
    @property
    def name(self) -> str:
        return "your_tool"
    
    @property
    def description(self) -> str:
        return "What your tool does"
    
    async def execute(self, **kwargs) -> ToolResult:
        # Your logic here
        return ToolResult(success=True, data={"result": "success"})
```

2. **Register It**
```python
# In tools/__init__.py
from .your_tool import YourTool
registry.register(YourTool())
```

## Security

- **Safe Evaluation**: Calculator uses AST parsing to prevent code injection
- **Input Validation**: All parameters validated before execution
- **Error Handling**: Comprehensive error handling prevents crashes
- **No Arbitrary Code**: Tools can't execute arbitrary user code

## Troubleshooting

**OpenAI API Key Issues**
- Check your `.env` file contains `OPENAI_API_KEY`
- Ensure your API key is valid and has credits
- Make sure the file isn't being ignored by git

**Tool Not Found Errors**
- Verify tools are registered in `tools/__init__.py`
- Check for import errors in your tool modules
- Restart the application after adding new tools

## Learning Resources

- [OpenAI Function Calling Docs](https://platform.openai.com/docs/guides/function-calling)
- [Rich Terminal Library](https://rich.readthedocs.io/)
- [Modern Python Typing](https://docs.python.org/3/library/typing.html)

## Contributing

Feel free to fork and submit PRs! This is a learning project, so all improvements welcome.

## License

MIT License - feel free to use this for your own learning projects.

## Shoutouts

Built for DSCubed Winter Program 2025 - thanks the AI team for the opportunity to learn function calling!

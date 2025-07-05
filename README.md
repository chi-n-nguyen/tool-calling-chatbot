# ai tool calling chatbot

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI GPT-4o-mini](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

a modular command-line ai assistant that integrates with openai's gpt-4o-mini model, featuring an extensible tool system for function calling.

## demo

```bash
# example interaction
$ chatbot

ai tool calling chatbot

you: calculate the area of a circle with radius 5
tool call: calculator(expression=3.14159 * 5 * 5)
result: 78.54
assistant: the area of a circle with radius 5 is approximately 78.54 square units.

you: generate a vintage outfit for a concert in winter
tool call: vintage_outfit_generator(occasion=concert, season=winter)
result: vintage melbourne core outfit with band tee, leather jacket, and doc martens
assistant: here's a perfect vintage melbourne outfit for a winter concert...

you: recommend a cheap restaurant for students
tool call: melbourne_food_recommender(budget=cheap, student=true)
result: dumplings plus on bourke street with student discount
assistant: i recommend dumplings plus on bourke street - great value and student discount available.
```

## features

- **function calling**: ai can automatically call predefined tools based on user requests
- **calculator**: safe mathematical expression evaluation with ast parsing
- **vintage outfit generator**: melbourne-focused vintage outfit recommendations
- **melbourne food recommender**: local restaurant suggestions with student discounts
- **rich cli**: beautiful terminal interface with colors and formatting
- **async support**: efficient asynchronous operations with concurrent tool execution
- **conversation history**: maintain chat context across interactions with persistent memory
- **type safety**: comprehensive type hints throughout the codebase using modern python typing
- **security**: input validation, safe code execution, and error handling

## quick start

### 1. prerequisites

- python 3.11 or higher
- openai api key ([get one here](https://platform.openai.com/api-keys))
- [uv](https://docs.astral.sh/uv/) for package management

### 2. installation

```bash
# clone the repository
git clone https://github.com/chi-n-nguyen/tool-calling-chatbot.git
cd tool-calling-chatbot

# install dependencies using uv
uv sync

# install the package in development mode
uv pip install -e .
```

### 3. configuration

create a `.env` file in the project root:

```bash
# copy the example environment file
cp .env.example .env

# edit the .env file with your api key
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. get your openai api key

1. visit [openai's api keys page](https://platform.openai.com/api-keys)
2. sign up or log in to your account
3. click "create new secret key"
4. copy the key and paste it into your `.env` file
5. **important**: add some credits to your openai account to use the api

### 5. run the chatbot

```bash
# method 1: using the installed command
chatbot

# method 2: using python directly  
python -m tool_calling_chatbot.main

# method 3: for development
uv run python -m tool_calling_chatbot.main
```

## usage examples

### calculator tool
```
you: calculate 2 + 3 * 4
assistant: i'll calculate that for you.
tool call: calculator(expression=2 + 3 * 4)
result: {'expression': '2 + 3 * 4', 'result': 14, 'formatted': '2 + 3 * 4 = 14'}
the result is 14.
```

### vintage outfit generator
```
you: generate a vintage melbourne outfit for a date in autumn
assistant: i'll create a vintage melbourne outfit for your autumn date.
tool call: vintage_outfit_generator(occasion=date, season=autumn)
result: vintage outfit with curated melbourne shopping spots
here's a perfect vintage melbourne outfit for your autumn date...
```

### melbourne food recommender
```
you: recommend a good restaurant for students on a budget
assistant: i'll find a great budget-friendly restaurant with student options.
tool call: melbourne_food_recommender(budget=cheap, student=true)
result: student-friendly restaurant recommendation with discount info
i recommend checking out these student-friendly spots in melbourne...
```

## available commands

| command | description |
|---------|-------------|
| `/help` | show help message |
| `/tools` | list available tools |
| `/history` | show conversation history |
| `/clear` | clear conversation history |
| `/exit` or `/quit` | exit the chatbot |

## available tools

### calculator
- **function**: `calculator`
- **description**: evaluates mathematical expressions safely
- **parameters**: `expression` (string) - mathematical expression to evaluate
- **example**: `"2 + 3 * 4"`, `"pow(2, 3)"`, `"abs(-5)"`

### vintage outfit generator
- **function**: `vintage_outfit_generator`
- **description**: generates vintage melbourne core outfit recommendations
- **parameters**: 
  - `occasion` (string, optional) - occasion for the outfit
  - `season` (string, optional) - melbourne season for appropriate layering
- **supported occasions**: casual, concert, date, uni, work, weekend
- **supported seasons**: summer, autumn, winter, spring

### melbourne food recommender
- **function**: `melbourne_food_recommender`
- **description**: recommends melbourne restaurants based on budget and preferences
- **parameters**: 
  - `budget` (string, optional) - budget preference for dining
  - `cuisine` (string, optional) - preferred cuisine type
  - `student` (boolean, optional) - whether user is a student seeking discounts

## project structure

```
tool-calling-chatbot/
├── src/
│   └── tool_calling_chatbot/
│       ├── __init__.py
│       ├── main.py              # main entry point
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py        # configuration management
│       │   ├── base.py          # base classes and registry
│       │   ├── openai_client.py # openai integration
│       │   └── cli.py           # cli interface
│       └── tools/
│           ├── __init__.py
│           ├── calculator.py    # calculator tool
│           ├── vintage_outfit_generator.py # outfit generator
│           └── melbourne_food_recommender.py # food recommender
├── pyproject.toml              # project configuration
├── .env.example               # environment template
├── .gitignore                # git ignore rules
└── README.md                 # this file
```

## development guide

### adding new tools

1. **create a new tool file** in `src/tool_calling_chatbot/tools/`:

```python
from typing import Any, List
from ..core.base import BaseTool, ToolParameter, ToolResult

class YourTool(BaseTool):
    @property
    def name(self) -> str:
        return "your_tool"
    
    @property
    def description(self) -> str:
        return "description of what your tool does"
    
    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="param_name",
                type="string",
                description="parameter description",
                required=True
            )
        ]
    
    async def execute(self, param_name: str) -> ToolResult:
        # your tool logic here
        return ToolResult(
            success=True,
            data={"result": "your_result"}
        )
```

2. **register the tool** in `src/tool_calling_chatbot/tools/__init__.py`:

```python
from .your_tool import YourTool

your_tool = YourTool()
registry.register(your_tool)
```

### environment variables

| variable | description | required | default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | openai api key | yes | - |
| `OPENAI_MODEL` | openai model to use | no | `gpt-4o-mini` |
| `OPENAI_TEMPERATURE` | response randomness (0.0-2.0) | no | `0.7` |
| `OPENAI_MAX_TOKENS` | maximum tokens per response | no | `1000` |

### running tests

```bash
# run with pytest (when tests are added)
uv run pytest

# run type checking
uv run mypy src/
```

## security features

- **safe expression evaluation**: calculator uses ast parsing to prevent code injection
- **input validation**: all tool parameters are validated before execution
- **error handling**: comprehensive error handling prevents crashes

## troubleshooting

### common issues

1. **"openai api key not found"**
   - check that your `.env` file exists and contains `OPENAI_API_KEY`
   - ensure the api key is valid and has credits

2. **"tool not found" errors**
   - verify all tools are properly registered in `tools/__init__.py`
   - check for import errors in tool modules

### debug mode

set environment variables for debugging:

```bash
export PYTHONPATH=src
export OPENAI_LOG_LEVEL=debug
```

## learning resources

- [openai function calling documentation](https://platform.openai.com/docs/guides/function-calling)
- [rich terminal library](https://rich.readthedocs.io/)
- [pydantic for data validation](https://pydantic-docs.helpmanual.io/)
- [modern python typing](https://docs.python.org/3/library/typing.html)

## contributing

1. fork the repository
2. create a feature branch
3. add your changes with proper type hints
4. test your changes
5. submit a pull request

## license

this project is licensed under the mit license.

## acknowledgments

- openai for the gpt-4o-mini model
- rich library for beautiful terminal output
- python community for excellent async support

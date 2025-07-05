"""Random joke tool for entertainment."""

import random
from typing import Any, List
from ..core.base import BaseTool, ToolParameter, ToolResult


class RandomJoke(BaseTool):
    """Random joke tool for entertainment."""
    
    PROGRAMMING_JOKES = [
        {
            "setup": "Why do programmers prefer dark mode?",
            "punchline": "Because light attracts bugs!",
            "category": "programming"
        },
        {
            "setup": "How many programmers does it take to change a light bulb?",
            "punchline": "None. That's a hardware problem.",
            "category": "programming"
        },
        {
            "setup": "Why did the programmer quit his job?",
            "punchline": "He didn't get arrays!",
            "category": "programming"
        },
        {
            "setup": "What's the object-oriented way to become wealthy?",
            "punchline": "Inheritance.",
            "category": "programming"
        },
        {
            "setup": "Why don't programmers like nature?",
            "punchline": "It has too many bugs.",
            "category": "programming"
        },
        {
            "setup": "What do you call a programmer from Finland?",
            "punchline": "Nerdic.",
            "category": "programming"
        },
        {
            "setup": "Why did the Python programmer not respond to the function call?",
            "punchline": "She was busy with other classes.",
            "category": "python"
        },
        {
            "setup": "What's a programmer's favorite hangout place?",
            "punchline": "Foo Bar.",
            "category": "programming"
        },
        {
            "setup": "Why do Java developers wear glasses?",
            "punchline": "Because they can't C#!",
            "category": "programming"
        },
        {
            "setup": "What's the best thing about a Boolean?",
            "punchline": "Even if you're wrong, you're only off by a bit.",
            "category": "programming"
        }
    ]
    
    GENERAL_JOKES = [
        {
            "setup": "Why don't scientists trust atoms?",
            "punchline": "Because they make up everything!",
            "category": "science"
        },
        {
            "setup": "What do you call a fake noodle?",
            "punchline": "An impasta!",
            "category": "food"
        },
        {
            "setup": "Why did the scarecrow win an award?",
            "punchline": "He was outstanding in his field!",
            "category": "general"
        },
        {
            "setup": "What do you call a bear with no teeth?",
            "punchline": "A gummy bear!",
            "category": "animals"
        },
        {
            "setup": "Why don't eggs tell jokes?",
            "punchline": "They'd crack each other up!",
            "category": "food"
        }
    ]
    
    @property
    def name(self) -> str:
        return "random_joke"
    
    @property
    def description(self) -> str:
        return "Tells a random joke to brighten your day! Can provide programming jokes or general jokes."
    
    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="category",
                type="string",
                description="Category of joke to tell",
                required=False,
                enum=["programming", "general", "any"]
            )
        ]
    
    async def execute(self, category: str = "any") -> ToolResult:
        """Execute the random joke tool."""
        try:
            # Select joke pool based on category
            if category == "programming":
                jokes = self.PROGRAMMING_JOKES
            elif category == "general":
                jokes = self.GENERAL_JOKES
            else:  # "any" or invalid category
                jokes = self.PROGRAMMING_JOKES + self.GENERAL_JOKES
            
            # Select random joke
            joke = random.choice(jokes)
            
            return ToolResult(
                success=True,
                data={
                    "setup": joke["setup"],
                    "punchline": joke["punchline"],
                    "category": joke["category"],
                    "full_joke": f"{joke['setup']} {joke['punchline']}"
                }
            )
            
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error getting joke: {str(e)}"
            ) 
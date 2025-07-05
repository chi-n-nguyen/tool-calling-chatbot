"""command-line interface for the tool calling chatbot."""

import asyncio
import sys
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown

from .config import Config
from .openai_client import OpenAIClient
from ..tools import registry


class ChatbotCLI:
    """command-line interface for the chatbot."""
    
    def __init__(self, config: Config):
        self.config = config
        self.console = Console()
        self.openai_client = OpenAIClient(config, registry)
        self.commands = {
            "/help": self._show_help,
            "/tools": self._show_tools,
            "/history": self._show_history,
            "/clear": self._clear_history,
            "/exit": self._exit,
            "/quit": self._exit,
        }
    
    def _print_welcome(self) -> None:
        """print welcome message."""
        welcome_text = """
        # 🤍 ai tool calling chatbot
        
        hey there! welcome to your friendly ai assistant with some handy tools to help you out.
        
        **what can i help you with today?**
        - `/help` 🤎 show this help message
        - `/tools` 🤍 list available tools
        - `/history` 🤍 show conversation history
        - `/clear` 🤍 clear conversation history
        - `/exit` or `/quit` 🤍 exit the chatbot
        
        **tools i can use for you:**
        - `calculator` 🤍 perform mathematical calculations
        - `vintage_outfit_generator` 🤎 generate vintage narrm core outfits
        - `narrm_food_recommender` 🤍 recommend narrm restaurants
        
        just ask me anything or request one of these tools - i'm here to help!
        """
        
        self.console.print(Panel(
            Markdown(welcome_text),
            title="🤍 welcome friend",
            border_style="bright_white"
        ))
    
    def _show_help(self) -> None:
        """show help message."""
        help_text = """
        ## available commands:
        
        - `/help` 🤍 show this help message
        - `/tools` 🤍 list available tools with descriptions
        - `/history` 🤍 show conversation history
        - `/clear` 🤍 clear conversation history
        - `/exit` or `/quit` 🤍 exit the chatbot
        
        ## how to use:
        
        1. **ask questions** 🤍 just type your question naturally
        2. **use tools** 🤍 ask me to calculate, generate outfits, or recommend food
        3. **examples**:
           - "calculate 2 + 3 * 4"
           - "generate a vintage outfit for a concert in winter"
           - "recommend a cheap restaurant for students"
        
        the ai will automatically choose the right tool for your request.
        """
        
        self.console.print(Panel(
            Markdown(help_text),
            title="🤍 help",
            border_style="bright_white"
        ))
    
    def _show_tools(self) -> None:
        """show available tools."""
        tools = registry.get_all()
        
        table = Table(title="🤍 available tools")
        table.add_column("tool name", style="bright_white", no_wrap=True)
        table.add_column("description", style="white")
        table.add_column("parameters", style="yellow")
        
        for name, tool in tools.items():
            params = ", ".join([
                f"{p.name}({p.type})" + ("*" if p.required else "")
                for p in tool.parameters
            ])
            table.add_row(name, tool.description, params)
        
        self.console.print(table)
        self.console.print("\n[italic yellow]* = required parameter[/italic yellow]")
    
    def _show_history(self) -> None:
        """show conversation history."""
        history = self.openai_client.get_conversation_history()
        
        if not history:
            self.console.print("[yellow]no conversation history yet.[/yellow]")
            return
        
        self.console.print(Panel(
            f"[bold]conversation history ({len(history)} messages)[/bold]",
            border_style="bright_white"
        ))
        
        for i, message in enumerate(history, 1):
            role = message["role"]
            content = message.get("content", "")
            
            # style based on role
            if role == "user":
                style = "bright_white"
                prefix = "🤍 you"
            elif role == "assistant":
                style = "bright_white"
                prefix = "🤍 assistant"
            elif role == "tool":
                style = "yellow"
                prefix = "🤍 tool"
            else:
                style = "white"
                prefix = role
            
            self.console.print(f"\n[{style}]{prefix}:[/{style}]")
            if content:
                self.console.print(f"  {content}")
            
            # show tool calls if present
            if "tool_calls" in message:
                for tool_call in message["tool_calls"]:
                    func_name = tool_call["function"]["name"]
                    args = tool_call["function"]["arguments"]
                    self.console.print(f"  [dim]🤍 tool called: {func_name}({args})[/dim]")
    
    def _clear_history(self) -> None:
        """clear conversation history."""
        self.openai_client.clear_history()
        self.console.print("[bright_white]🤍 conversation history cleared.[/bright_white]")
    
    def _exit(self) -> None:
        """exit the chatbot."""
        self.console.print("[bright_white]🤍 thanks for chatting! see you later.[/bright_white]")
        sys.exit(0)
    
    def _print_user_input(self, message: str) -> None:
        """print user input with styling."""
        self.console.print(f"\n[bright_white]🤍 you:[/bright_white] {message}")
    
    def _print_assistant_response(self, response: str) -> None:
        """print assistant response with styling."""
        self.console.print(f"\n[bright_white]🤍 assistant:[/bright_white]")
        self.console.print(f"  {response}")
    
    def _print_tool_calls(self, tool_results: List[Dict[str, Any]]) -> None:
        """print tool call results."""
        for tool_result in tool_results:
            function_name = tool_result["function_name"]
            arguments = tool_result["arguments"]
            result = tool_result["result"]
            
            # format arguments
            args_str = ", ".join([f"{k}={v}" for k, v in arguments.items()])
            
            self.console.print(f"\n[yellow]🤍 tool call:[/yellow] {function_name}({args_str})")
            
            if result["success"]:
                self.console.print(f"[bright_white]🤍 result:[/bright_white] {result['data']}")
            else:
                self.console.print(f"[red]🤍 error:[/red] {result['error']}")
    
    def _print_error(self, error: str) -> None:
        """print error message."""
        self.console.print(f"\n[red]🤍 error:[/red] {error}")
    
    async def _handle_user_input(self, user_input: str) -> None:
        """handle user input and get ai response."""
        try:
            # show typing indicator
            with self.console.status("[bright_white]🤍 thinking...[/bright_white]"):
                response_data = await self.openai_client.chat_completion(user_input)
            
            # print tool calls if any
            if response_data["tool_calls"]:
                self._print_tool_calls(response_data["tool_results"])
            
            # print assistant response
            if response_data["response"]:
                self._print_assistant_response(response_data["response"])
            
        except Exception as e:
            self._print_error(f"failed to get response: {str(e)}")
    
    async def run(self) -> None:
        """run the chatbot cli."""
        self._print_welcome()
        
        while True:
            try:
                # get user input
                user_input = Prompt.ask("\n[bright_white]🤍 you[/bright_white]", default="").strip()
                
                # check for empty input
                if not user_input:
                    continue
                
                # handle commands
                if user_input.startswith('/'):
                    command = user_input.lower()
                    if command in self.commands:
                        self.commands[command]()
                    else:
                        self.console.print(f"[red]🤍 unknown command: {user_input}[/red]")
                        self.console.print("[yellow]🤍 type /help for available commands.[/yellow]")
                    continue
                
                # print user input
                self._print_user_input(user_input)
                
                # handle regular chat
                await self._handle_user_input(user_input)
                
            except KeyboardInterrupt:
                self.console.print("\n[bright_white]🤍 goodbye![/bright_white]")
                break
            except EOFError:
                self.console.print("\n[bright_white]🤍 goodbye![/bright_white]")
                break
            except Exception as e:
                self._print_error(f"unexpected error: {str(e)}")


async def main() -> None:
    """main entry point for the cli."""
    try:
        config = Config.from_env()
        config.validate()
        
        cli = ChatbotCLI(config)
        await cli.run()
        
    except ValueError as e:
        console = Console()
        console.print(f"[red]🤍 configuration error:[/red] {str(e)}")
        console.print("[yellow]🤍 please check your .env file or environment variables.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console = Console()
        console.print(f"[red]🤍 unexpected error:[/red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 
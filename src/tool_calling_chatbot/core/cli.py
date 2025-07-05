"""Command-line interface for the tool calling chatbot."""

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
    """Command-line interface for the chatbot."""
    
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
        """Print welcome message."""
        welcome_text = """
        # 🤖 AI Tool Calling Chatbot
        
        Welcome to your AI assistant with function calling capabilities!
        
        **Available Commands:**
        - `/help` - Show this help message
        - `/tools` - List available tools
        - `/history` - Show conversation history
        - `/clear` - Clear conversation history
        - `/exit` or `/quit` - Exit the chatbot
        
        **Available Tools:**
        - `calculator` - Perform mathematical calculations
        - `file_reader` - Read text files safely
        - `random_joke` - Get random jokes
        
        Start chatting or ask me to use any of the available tools!
        """
        
        self.console.print(Panel(
            Markdown(welcome_text),
            title="🚀 Welcome",
            border_style="blue"
        ))
    
    def _show_help(self) -> None:
        """Show help message."""
        help_text = """
        ## Available Commands:
        
        - `/help` - Show this help message
        - `/tools` - List available tools with descriptions
        - `/history` - Show conversation history
        - `/clear` - Clear conversation history
        - `/exit` or `/quit` - Exit the chatbot
        
        ## How to Use:
        
        1. **Ask questions**: Just type your question naturally
        2. **Use tools**: Ask me to calculate, read files, or tell jokes
        3. **Examples**:
           - "Calculate 2 + 3 * 4"
           - "Read the content of README.md"
           - "Tell me a programming joke"
        
        The AI will automatically choose the right tool for your request!
        """
        
        self.console.print(Panel(
            Markdown(help_text),
            title="📚 Help",
            border_style="green"
        ))
    
    def _show_tools(self) -> None:
        """Show available tools."""
        tools = registry.get_all()
        
        table = Table(title="🔧 Available Tools")
        table.add_column("Tool Name", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Parameters", style="yellow")
        
        for name, tool in tools.items():
            params = ", ".join([
                f"{p.name}({p.type})" + ("*" if p.required else "")
                for p in tool.parameters
            ])
            table.add_row(name, tool.description, params)
        
        self.console.print(table)
        self.console.print("\n[italic yellow]* = required parameter[/italic yellow]")
    
    def _show_history(self) -> None:
        """Show conversation history."""
        history = self.openai_client.get_conversation_history()
        
        if not history:
            self.console.print("[yellow]No conversation history yet.[/yellow]")
            return
        
        self.console.print(Panel(
            f"[bold]Conversation History ({len(history)} messages)[/bold]",
            border_style="blue"
        ))
        
        for i, message in enumerate(history, 1):
            role = message["role"]
            content = message.get("content", "")
            
            # Style based on role
            if role == "user":
                style = "blue"
                prefix = "👤 User"
            elif role == "assistant":
                style = "green"
                prefix = "🤖 Assistant"
            elif role == "tool":
                style = "yellow"
                prefix = "🔧 Tool"
            else:
                style = "white"
                prefix = f"📝 {role.title()}"
            
            self.console.print(f"\n[{style}]{prefix}:[/{style}]")
            if content:
                self.console.print(f"  {content}")
            
            # Show tool calls if present
            if "tool_calls" in message:
                for tool_call in message["tool_calls"]:
                    func_name = tool_call["function"]["name"]
                    args = tool_call["function"]["arguments"]
                    self.console.print(f"  [dim]🔧 Called: {func_name}({args})[/dim]")
    
    def _clear_history(self) -> None:
        """Clear conversation history."""
        self.openai_client.clear_history()
        self.console.print("[green]✅ Conversation history cleared.[/green]")
    
    def _exit(self) -> None:
        """Exit the chatbot."""
        self.console.print("[blue]👋 Goodbye! Thanks for using the AI Chatbot![/blue]")
        sys.exit(0)
    
    def _print_user_input(self, message: str) -> None:
        """Print user input with styling."""
        self.console.print(f"\n[blue]👤 You:[/blue] {message}")
    
    def _print_assistant_response(self, response: str) -> None:
        """Print assistant response with styling."""
        self.console.print(f"\n[green]🤖 Assistant:[/green]")
        self.console.print(f"  {response}")
    
    def _print_tool_calls(self, tool_results: List[Dict[str, Any]]) -> None:
        """Print tool call results."""
        for tool_result in tool_results:
            function_name = tool_result["function_name"]
            arguments = tool_result["arguments"]
            result = tool_result["result"]
            
            # Format arguments
            args_str = ", ".join([f"{k}={v}" for k, v in arguments.items()])
            
            self.console.print(f"\n[yellow]🔧 Tool Call:[/yellow] {function_name}({args_str})")
            
            if result["success"]:
                self.console.print(f"[green]✅ Result:[/green] {result['data']}")
            else:
                self.console.print(f"[red]❌ Error:[/red] {result['error']}")
    
    def _print_error(self, error: str) -> None:
        """Print error message."""
        self.console.print(f"\n[red]❌ Error:[/red] {error}")
    
    async def _handle_user_input(self, user_input: str) -> None:
        """Handle user input and get AI response."""
        try:
            # Show typing indicator
            with self.console.status("[blue]🤖 Thinking...[/blue]"):
                response_data = await self.openai_client.chat_completion(user_input)
            
            # Print tool calls if any
            if response_data["tool_calls"]:
                self._print_tool_calls(response_data["tool_results"])
            
            # Print assistant response
            if response_data["response"]:
                self._print_assistant_response(response_data["response"])
            
        except Exception as e:
            self._print_error(f"Failed to get response: {str(e)}")
    
    async def run(self) -> None:
        """Run the chatbot CLI."""
        self._print_welcome()
        
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("\n[blue]💬 You[/blue]", default="").strip()
                
                # Check for empty input
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    command = user_input.lower()
                    if command in self.commands:
                        self.commands[command]()
                    else:
                        self.console.print(f"[red]❌ Unknown command: {user_input}[/red]")
                        self.console.print("[yellow]💡 Type /help for available commands.[/yellow]")
                    continue
                
                # Print user input
                self._print_user_input(user_input)
                
                # Handle regular chat
                await self._handle_user_input(user_input)
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]👋 Goodbye![/yellow]")
                break
            except EOFError:
                self.console.print("\n[yellow]👋 Goodbye![/yellow]")
                break
            except Exception as e:
                self._print_error(f"Unexpected error: {str(e)}")


async def main() -> None:
    """Main entry point for the CLI."""
    try:
        config = Config.from_env()
        config.validate()
        
        cli = ChatbotCLI(config)
        await cli.run()
        
    except ValueError as e:
        console = Console()
        console.print(f"[red]❌ Configuration Error:[/red] {str(e)}")
        console.print("[yellow]💡 Please check your .env file or environment variables.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console = Console()
        console.print(f"[red]❌ Unexpected Error:[/red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 
"""Main entry point for the tool calling chatbot."""

import asyncio
import sys
from .core.cli import main as cli_main


def main():
    """Main entry point for the chatbot application."""
    try:
        # Run the CLI
        asyncio.run(cli_main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
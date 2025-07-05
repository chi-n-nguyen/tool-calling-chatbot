"""OpenAI client for function calling integration."""

import json
import asyncio
from typing import Any, Dict, List, Optional, Union
from openai import AsyncOpenAI
from .config import Config
from .base import ToolRegistry, ToolResult


class OpenAIClient:
    """Async OpenAI client with function calling support."""
    
    def __init__(self, config: Config, tool_registry: ToolRegistry):
        self.config = config
        self.tool_registry = tool_registry
        self.client = AsyncOpenAI(api_key=config.openai_api_key)
        self.conversation_history: List[Dict[str, Any]] = []
    
    def add_message(self, role: str, content: str, tool_calls: Optional[List[Dict]] = None) -> None:
        """Add a message to the conversation history."""
        message = {"role": role, "content": content}
        if tool_calls:
            message["tool_calls"] = tool_calls
        self.conversation_history.append(message)
    
    def add_tool_result(self, tool_call_id: str, result: ToolResult) -> None:
        """Add a tool result to the conversation history."""
        content = json.dumps(result.to_dict()) if result.success else result.error
        self.conversation_history.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": content
        })
    
    async def chat_completion(self, message: str) -> Dict[str, Any]:
        """Get a chat completion with function calling support."""
        try:
            # Add user message to history
            self.add_message("user", message)
            
            # Get available tools
            tools = self.tool_registry.get_schemas()
            
            # Make the API call
            response = await self.client.chat.completions.create(
                model=self.config.model,
                messages=self.conversation_history,
                tools=tools if tools else None,
                tool_choice="auto" if tools else None,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            # Extract the response
            assistant_message = response.choices[0].message
            
            # Handle function calls
            if assistant_message.tool_calls:
                # Add assistant message with tool calls
                self.add_message(
                    "assistant",
                    assistant_message.content or "",
                    [tc.model_dump() for tc in assistant_message.tool_calls]
                )
                
                # Execute tool calls
                tool_results = await self._execute_tool_calls(assistant_message.tool_calls)
                
                # Make another API call to get the final response
                final_response = await self.client.chat.completions.create(
                    model=self.config.model,
                    messages=self.conversation_history,
                    tools=tools if tools else None,
                    tool_choice="auto" if tools else None,
                    temperature=self.config.temperature,
                    max_tokens=self.config.max_tokens
                )
                
                final_message = final_response.choices[0].message
                self.add_message("assistant", final_message.content or "")
                
                return {
                    "response": final_message.content,
                    "tool_calls": assistant_message.tool_calls,
                    "tool_results": tool_results,
                    "usage": final_response.usage.model_dump() if final_response.usage else None
                }
            else:
                # No tool calls, just add the assistant response
                self.add_message("assistant", assistant_message.content or "")
                
                return {
                    "response": assistant_message.content,
                    "tool_calls": None,
                    "tool_results": None,
                    "usage": response.usage.model_dump() if response.usage else None
                }
                
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
    
    async def _execute_tool_calls(self, tool_calls) -> List[Dict[str, Any]]:
        """Execute multiple tool calls concurrently."""
        async def execute_single_tool(tool_call):
            try:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute the tool
                result = await self.tool_registry.execute(function_name, **function_args)
                
                # Add tool result to conversation history
                self.add_tool_result(tool_call.id, result)
                
                return {
                    "tool_call_id": tool_call.id,
                    "function_name": function_name,
                    "arguments": function_args,
                    "result": result.to_dict()
                }
                
            except Exception as e:
                error_result = ToolResult(
                    success=False,
                    error=f"Tool execution error: {str(e)}"
                )
                self.add_tool_result(tool_call.id, error_result)
                
                return {
                    "tool_call_id": tool_call.id,
                    "function_name": tool_call.function.name,
                    "arguments": {},
                    "result": error_result.to_dict()
                }
        
        # Execute all tool calls concurrently
        tasks = [execute_single_tool(tc) for tc in tool_calls]
        return await asyncio.gather(*tasks)
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get the current conversation history."""
        return self.conversation_history.copy()
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history.clear()
    
    def get_tools_info(self) -> Dict[str, Any]:
        """Get information about available tools."""
        tools = self.tool_registry.get_all()
        return {
            "total_tools": len(tools),
            "tool_names": list(tools.keys()),
            "tool_descriptions": {name: tool.description for name, tool in tools.items()}
        } 
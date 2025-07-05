"""Base classes for the tool calling system."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol, TypeAlias
from pydantic import BaseModel, Field
import json


# Type aliases for better readability
ToolParameters: TypeAlias = Dict[str, Any]
ToolResult: TypeAlias = Dict[str, Any]


class ToolParameter(BaseModel):
    """Schema for a tool parameter."""
    
    name: str
    type: str
    description: str
    required: bool = True
    enum: Optional[List[str]] = None


class ToolSchema(BaseModel):
    """Schema for a tool definition."""
    
    name: str
    description: str
    parameters: List[ToolParameter]


class ToolResult(BaseModel):
    """Result from a tool execution."""
    
    success: bool
    data: Any = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
        }


class BaseTool(ABC):
    """Abstract base class for all tools."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the tool name."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Get the tool description."""
        pass
    
    @property
    @abstractmethod
    def parameters(self) -> List[ToolParameter]:
        """Get the tool parameters."""
        pass
    
    @abstractmethod
    async def execute(self, **kwargs: Any) -> ToolResult:
        """Execute the tool with given parameters."""
        pass
    
    def get_schema(self) -> ToolSchema:
        """Get the tool schema for OpenAI function calling."""
        return ToolSchema(
            name=self.name,
            description=self.description,
            parameters=self.parameters
        )
    
    def get_openai_schema(self) -> Dict[str, Any]:
        """Get the OpenAI-compatible function schema."""
        properties = {}
        required = []
        
        for param in self.parameters:
            prop = {
                "type": param.type,
                "description": param.description
            }
            if param.enum:
                prop["enum"] = param.enum
            
            properties[param.name] = prop
            if param.required:
                required.append(param.name)
        
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }


class ToolRegistry:
    """Registry for managing tools."""
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
    
    def register(self, tool: BaseTool) -> None:
        """Register a tool."""
        self._tools[tool.name] = tool
    
    def get(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def get_all(self) -> Dict[str, BaseTool]:
        """Get all registered tools."""
        return self._tools.copy()
    
    def get_schemas(self) -> List[Dict[str, Any]]:
        """Get OpenAI-compatible schemas for all tools."""
        return [tool.get_openai_schema() for tool in self._tools.values()]
    
    def list_tools(self) -> List[str]:
        """List all tool names."""
        return list(self._tools.keys())
    
    async def execute(self, name: str, **kwargs: Any) -> ToolResult:
        """Execute a tool by name."""
        tool = self.get(name)
        if not tool:
            return ToolResult(
                success=False,
                error=f"Tool '{name}' not found"
            )
        
        try:
            return await tool.execute(**kwargs)
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error executing tool '{name}': {str(e)}"
            )


# Global registry instance
registry = ToolRegistry() 
"""File reader tool for reading text files safely."""

import os
from pathlib import Path
from typing import Any, List
from ..core.base import BaseTool, ToolParameter, ToolResult


class FileReader(BaseTool):
    """Safe file reader tool for reading text files."""
    
    # Maximum file size (1MB)
    MAX_FILE_SIZE = 1024 * 1024
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.yaml', '.yml', '.xml'}
    
    @property
    def name(self) -> str:
        return "file_reader"
    
    @property
    def description(self) -> str:
        return "Reads the contents of text files safely. Supports common text file formats."
    
    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="file_path",
                type="string",
                description="Path to the file to read (relative or absolute path)",
                required=True
            ),
            ToolParameter(
                name="max_lines",
                type="integer",
                description="Maximum number of lines to read (default: 100, max: 1000)",
                required=False
            )
        ]
    
    def _is_safe_file(self, file_path: Path) -> tuple[bool, str]:
        """Check if the file is safe to read."""
        try:
            # Check if file exists
            if not file_path.exists():
                return False, f"File does not exist: {file_path}"
            
            # Check if it's actually a file
            if not file_path.is_file():
                return False, f"Path is not a file: {file_path}"
            
            # Check file size
            file_size = file_path.stat().st_size
            if file_size > self.MAX_FILE_SIZE:
                return False, f"File too large: {file_size} bytes (max: {self.MAX_FILE_SIZE})"
            
            # Check file extension
            if file_path.suffix.lower() not in self.ALLOWED_EXTENSIONS:
                return False, f"File type not allowed: {file_path.suffix}"
            
            return True, "File is safe to read"
            
        except Exception as e:
            return False, f"Error checking file: {str(e)}"
    
    async def execute(self, file_path: str, max_lines: int = 100) -> ToolResult:
        """Execute the file reader tool."""
        try:
            # Validate max_lines parameter
            if max_lines <= 0:
                max_lines = 100
            elif max_lines > 1000:
                max_lines = 1000
            
            # Convert to Path object
            path = Path(file_path).resolve()
            
            # Security check
            is_safe, message = self._is_safe_file(path)
            if not is_safe:
                return ToolResult(
                    success=False,
                    error=message
                )
            
            # Read the file
            with open(path, 'r', encoding='utf-8') as file:
                lines = []
                for i, line in enumerate(file):
                    if i >= max_lines:
                        break
                    lines.append(line.rstrip('\n\r'))
                
                content = '\n'.join(lines)
                
                # Check if we truncated the file
                truncated = False
                try:
                    # Check if there are more lines
                    next_line = file.readline()
                    if next_line:
                        truncated = True
                except:
                    pass
            
            return ToolResult(
                success=True,
                data={
                    "file_path": str(path),
                    "content": content,
                    "lines_read": len(lines),
                    "truncated": truncated,
                    "file_size": path.stat().st_size
                }
            )
            
        except UnicodeDecodeError:
            return ToolResult(
                success=False,
                error="File contains non-text content or unsupported encoding"
            )
        except PermissionError:
            return ToolResult(
                success=False,
                error="Permission denied: Cannot read file"
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Error reading file: {str(e)}"
            ) 
"""Calculator tool for mathematical expression evaluation."""

import ast
import operator
from typing import Any, List
from ..core.base import BaseTool, ToolParameter, ToolResult


class Calculator(BaseTool):
    """Safe calculator tool for mathematical expressions."""
    
    # Safe operations mapping
    SAFE_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
        ast.Mod: operator.mod,
    }
    
    # Safe functions
    SAFE_FUNCTIONS = {
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'sum': sum,
        'pow': pow,
    }
    
    @property
    def name(self) -> str:
        return "calculator"
    
    @property
    def description(self) -> str:
        return "Evaluates mathematical expressions safely. Supports basic arithmetic, powers, and common functions."
    
    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="expression",
                type="string",
                description="Mathematical expression to evaluate (e.g., '2 + 3 * 4', 'pow(2, 3)', 'abs(-5)')",
                required=True
            )
        ]
    
    def _safe_eval(self, node: ast.AST) -> Any:
        """Safely evaluate an AST node."""
        if isinstance(node, ast.Expression):
            return self._safe_eval(node.body)
        
        elif isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        
        elif isinstance(node, ast.Num):  # Python < 3.8
            return node.n
        
        elif isinstance(node, ast.BinOp):
            left = self._safe_eval(node.left)
            right = self._safe_eval(node.right)
            op = self.SAFE_OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operation: {type(node.op).__name__}")
            return op(left, right)
        
        elif isinstance(node, ast.UnaryOp):
            operand = self._safe_eval(node.operand)
            op = self.SAFE_OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported unary operation: {type(node.op).__name__}")
            return op(operand)
        
        elif isinstance(node, ast.Call):
            func_name = node.func.id if isinstance(node.func, ast.Name) else None
            if func_name not in self.SAFE_FUNCTIONS:
                raise ValueError(f"Unsupported function: {func_name}")
            
            args = [self._safe_eval(arg) for arg in node.args]
            return self.SAFE_FUNCTIONS[func_name](*args)
        
        elif isinstance(node, ast.Name):
            # Only allow certain constants
            if node.id in ('pi', 'e'):
                import math
                return getattr(math, node.id)
            raise ValueError(f"Unsupported name: {node.id}")
        
        else:
            raise ValueError(f"Unsupported AST node type: {type(node).__name__}")
    
    async def execute(self, expression: str) -> ToolResult:
        """Execute the calculator tool."""
        try:
            # Parse the expression
            parsed = ast.parse(expression, mode='eval')
            
            # Evaluate safely
            result = self._safe_eval(parsed)
            
            # Format the result
            if isinstance(result, float):
                # Round to reasonable precision
                result = round(result, 10)
            
            return ToolResult(
                success=True,
                data={
                    "expression": expression,
                    "result": result,
                    "formatted": f"{expression} = {result}"
                }
            )
            
        except SyntaxError as e:
            return ToolResult(
                success=False,
                error=f"Invalid mathematical expression: {str(e)}"
            )
        except ZeroDivisionError:
            return ToolResult(
                success=False,
                error="Division by zero is not allowed"
            )
        except ValueError as e:
            return ToolResult(
                success=False,
                error=str(e)
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Calculation error: {str(e)}"
            ) 
"""Calculator tool for mathematical computations."""
import math
import operator
from typing import Dict, Any


class CalculatorTool:
    """Tool for performing mathematical calculations safely."""
    
    # Safe operations allowed
    SAFE_OPERATIONS = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "//": operator.floordiv,
        "%": operator.mod,
        "**": operator.pow,
        "pow": pow,
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
    }
    
    # Safe functions from math module
    SAFE_FUNCTIONS = {
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "log10": math.log10,
        "exp": math.exp,
        "ceil": math.ceil,
        "floor": math.floor,
        "pi": math.pi,
        "e": math.e,
    }
    
    def calculate(self, expression: str) -> Dict[str, Any]:
        """
        Safely evaluate a mathematical expression.
        
        Args:
            expression: Mathematical expression as string
            
        Returns:
            Dictionary with calculation result
        """
        try:
            # Create safe evaluation context
            safe_dict = {**self.SAFE_OPERATIONS, **self.SAFE_FUNCTIONS}
            safe_dict["__builtins__"] = {}
            
            # Evaluate expression
            result = eval(expression, safe_dict, {})
            
            return {
                "expression": expression,
                "result": result,
                "formatted": f"{result:,.2f}" if isinstance(result, float) else str(result)
            }
            
        except ZeroDivisionError:
            return {
                "error": "Division by zero",
                "expression": expression,
                "result": None
            }
        except Exception as e:
            return {
                "error": f"Calculation error: {str(e)}",
                "expression": expression,
                "result": None
            }
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """Get tool definition for Claude function calling."""
        return {
            "name": "calculator",
            "description": "Perform mathematical calculations and computations. Use this when the user asks for calculations, percentages, conversions, or any mathematical operations.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '25 * 84', '15% of 2450', 'sqrt(144)')"
                    }
                },
                "required": ["expression"]
            }
        }


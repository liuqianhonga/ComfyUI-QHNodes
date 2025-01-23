from .lib import ANY

class DynamicExpressionNode:
    """Node that executes dynamic Python expressions with given arguments"""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "expression": ("STRING", {"multiline": True, "default": "# Example:\n# return arg1 + arg2"}),
            },
            "optional": {
                "arg1": (ANY, ),
                "arg2": (ANY, ),
                "arg3": (ANY, ),
                "arg4": (ANY, ),
                "arg5": (ANY, ),
            }
        }
    
    RETURN_TYPES = (ANY,)
    FUNCTION = "execute_expression"
    CATEGORY = "🐟QHNodes"

    def execute_expression(self, expression, arg1=None, arg2=None, arg3=None, arg4=None, arg5=None):
        """Execute the given expression with provided arguments"""
        try:            
            # Create a local scope with the arguments
            local_vars = {
                'arg1': arg1,
                'arg2': arg2,
                'arg3': arg3,
                'arg4': arg4,
                'arg5': arg5,
                'result': None  # Initialize result variable
            }
            
            # Execute the expression in a restricted scope
            # Compile the expression first to catch syntax errors
            # Add result assignment if not present in expression
            if 'result' not in expression:
                expression = expression + "\nresult = " + expression
            
            compiled_code = compile(expression, '<string>', 'exec')
                        
            # Execute the code
            exec(compiled_code, {"__builtins__": __builtins__}, local_vars)

            # Check if there's a return value defined
            if 'result' in local_vars:
                return (local_vars['result'],)
            else:
                return (None,)
                
        except Exception as e:
            return (None,) 
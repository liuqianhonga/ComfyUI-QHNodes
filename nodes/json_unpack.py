import json
from typing import Tuple
from .lib import ANY

class JsonUnpack:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_string": ("STRING", {"default": "{}"}),
                "key1": ("STRING", {"default": ""}),
            },
            "optional": {
                "key2": ("STRING", {"default": None}),
                "key3": ("STRING", {"default": None}),
                "key4": ("STRING", {"default": None}),
                "key5": ("STRING", {"default": None}),
            }
        }

    # Use ANY type from lib.py for flexible output connections
    RETURN_TYPES = tuple([ANY] * 5)  # Use lib.py's ANY for flexible output connections
    # Name outputs as value1 to value5
    RETURN_NAMES = tuple([f"value{i}" for i in range(1, 6)])  # Outputs are named value1 to value5
    FUNCTION = "unpack_json"
    CATEGORY = "🐟QHNodes"

    def unpack_json(self, json_string: str, key1: str, 
                   key2: str = None, key3: str = None, key4: str = None, key5: str = None) -> Tuple:
        try:
            # Parse JSON string
            data = json.loads(json_string)
            
            # Collect all keys
            keys = [key1, key2, key3, key4, key5]
            
            # Get values (return None for unspecified keys)
            values = []
            for key in keys:
                if key:  # If key is not empty
                    values.append(data.get(key))
                else:
                    values.append(None)
            
            return tuple(values)
            
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON string: {json_string}")
            return tuple([None] * 5)
        except Exception as e:
            print(f"Error unpacking JSON: {str(e)}")
            return tuple([None] * 5)

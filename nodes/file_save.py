import os
from .lib import FILE_TYPES

class FileSave:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "content": ("STRING", {"multiline": True}),
                "filename": ("STRING", {"default": "output"}),
                "filetype": (FILE_TYPES, {"default": "txt"}),
                "folder": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("filepath",)
    FUNCTION = "save_file"
    CATEGORY = "🐟QHNodes"

    def save_file(self, content, filename, filetype, folder):
        # Create folder if it doesn't exist
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except Exception as e:
                print(f"Error creating directory {folder}: {str(e)}")
                return ("",)

        # Clean filename and ensure it has the correct extension
        clean_filename = filename.strip()
        if not clean_filename:
            clean_filename = "output"
        
        # Remove extension if present
        clean_filename = os.path.splitext(clean_filename)[0]
        
        # Add the correct extension
        full_filename = f"{clean_filename}.{filetype}"
        
        # Create full file path
        filepath = os.path.join(folder, full_filename)
        
        try:
            # Write content to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return (filepath,)
        except Exception as e:
            print(f"Error saving file {filepath}: {str(e)}")
            return ("",)

import os
import folder_paths

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

ANY = AnyType("*")

class LoadLoraFromFolder:
    def __init__(self):
        self.lora_path = folder_paths.models_dir + "/loras"
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "lora_folders": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Multiple folders separated by comma (,)"
                }),
                "filter_text": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Multiple filter texts separated by comma (,)"
                }),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01}),
            }
        }
    
    RETURN_TYPES = (ANY, "FLOAT",)
    RETURN_NAMES = ("loras", "strength")
    OUTPUT_IS_LIST = (True, False)
    FUNCTION = "load_loras"
    CATEGORY = "QHNodes"

    def load_loras(self, lora_folders, filter_text="", strength_model=0):
        # Split lora_folders into multiple paths
        folders = [p.strip() for p in lora_folders.split(',') if p.strip()]
        if not folders:
            raise ValueError("No valid folder provided")

        # Split filter text into list
        filters = [f.strip().lower() for f in filter_text.split(',') if f.strip()]
        
        lora_files = []
        for folder in folders:
            # Build full path
            full_path = os.path.join(self.lora_path, folder)
            
            # Check if path exists
            if not os.path.exists(full_path):
                print(f"Path not found: {full_path}")
                continue
            
            # Iterate through all files in directory
            for file in os.listdir(full_path):
                if file.endswith('.safetensors'):
                    if not filters or any(f.lower() in file.lower() for f in filters):
                        relative_path = os.path.join(folder, file)
                        lora_files.append(relative_path)
        
        return {"ui": {"loras": [lora_files]}, "result": (lora_files, strength_model)}
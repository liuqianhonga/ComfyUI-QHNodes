import os
import folder_paths
import comfy.utils
import comfy.sd
from .lib import ANY

class LoadLoraFromFolder:
    def __init__(self):
        self.lora_path = folder_paths.models_dir + "/loras"
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": ("MODEL",),
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
                "merge_loras": ("BOOLEAN", {"default": False}),
            }
        }
    
    RETURN_TYPES = ("MODEL", ANY, "FLOAT")
    RETURN_NAMES = ("models", "loras", "strength")
    OUTPUT_IS_LIST = (True, True, False)
    FUNCTION = "load_loras"
    CATEGORY = "QHNodes"

    def load_loras(self, model, lora_folders, filter_text="", strength_model=1.0, merge_loras=False):
        """Load LoRA models from specified folders"""
        try:
            # Split lora_folders into multiple paths
            if not lora_folders:
                folders = [self.lora_path]  # Use default path
            else:
                folders = []
                for p in lora_folders.split(','):
                    p = p.strip()
                    if not p:
                        continue
                    # Handle absolute and relative paths
                    if os.path.isabs(p):
                        folders.append(p)  # Use absolute path directly
                    else:
                        folders.append(os.path.join(self.lora_path, p))  # Join relative path with default path
            
            # Split filter text into list
            filters = [f.strip().lower() for f in filter_text.split(',') if f.strip()]
            
            lora_files = []
            for folder in folders:
                if os.path.exists(folder):
                    for file in os.listdir(folder):
                        if file.endswith(('.safetensors', '.ckpt')):
                            # Apply filters if any
                            if filters:
                                file_lower = file.lower()
                                if not any(f in file_lower for f in filters):
                                    continue
                            lora_files.append(os.path.join(folder, file))
            
            # Raise exception if no LoRA files found
            if not lora_files:
                if filters:
                    print(f"[Load LoRA] No LoRA files found matching filters: {filters} in folders: {folders}")
                else:
                    print(f"[Load LoRA] No LoRA files found in folders: {folders}")
                raise ValueError(f"No LoRA files found in folders: {folders}")
            
            # Load all LoRA files
            loaded_loras = []
            for file in lora_files:
                try:
                    lora_name = os.path.splitext(os.path.basename(file))[0]
                    loaded_loras.append({
                        "name": lora_name,
                        "path": file
                    })
                except Exception as e:
                    print(f"[Load LoRA] Error loading {file}: {str(e)}")
                    continue
            
            if not loaded_loras:
                if filters:
                    raise ValueError(f"No LoRA files found matching filters: {filter_text}")
                else:
                    raise ValueError("No LoRA files found in the specified folders")

            # Load LoRAs
            if merge_loras:
                # Merge all LoRAs into a single model
                result_model = model.clone()
                for lora_file in lora_files:
                    full_path = lora_file
                    lora = comfy.utils.load_torch_file(full_path)
                    result_model = comfy.sd.load_lora_for_models(result_model, None, lora, strength_model, 0)[0]
                models = [result_model]
                # Join lora_files for result while preserving original list for UI
                combined_loras = " ".join(lora_files)
                return {"ui": {"loras": [lora_files]}, "result": (models, [combined_loras], strength_model)}
            else:
                # Load each LoRA into its own model clone
                models = []
                for lora_file in lora_files:
                    model_clone = model.clone()
                    full_path = lora_file
                    lora = comfy.utils.load_torch_file(full_path)
                    model_clone = comfy.sd.load_lora_for_models(model_clone, None, lora, strength_model, 0)[0]
                    models.append(model_clone)
                
                return {"ui": {"loras": [lora_files]}, "result": (models, lora_files, strength_model)}
            
        except Exception as e:
            print(f"[Load LoRA] Error: {str(e)}")
            raise ValueError(f"Error loading LoRAs: {str(e)}")
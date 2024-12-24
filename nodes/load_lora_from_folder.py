import os
import folder_paths
import comfy.utils
import comfy.sd

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

        if not lora_files:
            if filters:
                raise ValueError(f"No LoRA files found matching filters: {filter_text}")
            else:
                raise ValueError("No LoRA files found in the specified folders")

        # Load LoRAs
        if merge_loras:
            # Load all LoRAs into the same model
            result_model = model.clone()
            for lora_file in lora_files:
                full_path = os.path.join(self.lora_path, lora_file)
                lora = comfy.utils.load_torch_file(full_path)
                result_model = comfy.sd.load_lora_for_models(result_model, None, lora, strength_model, 0)[0]
            models = [result_model]
            # Combine lora_files into a single string for result, but keep original list for UI
            combined_loras = " ".join(lora_files)
            return {"ui": {"loras": [lora_files]}, "result": (models, [combined_loras], strength_model)}
        else:
            # Load each LoRA into a separate model clone
            models = []
            for lora_file in lora_files:
                model_clone = model.clone()
                full_path = os.path.join(self.lora_path, lora_file)
                lora = comfy.utils.load_torch_file(full_path)
                model_clone = comfy.sd.load_lora_for_models(model_clone, None, lora, strength_model, 0)[0]
                models.append(model_clone)
            
            return {"ui": {"loras": [lora_files]}, "result": (models, lora_files, strength_model)}
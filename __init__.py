from .nodes.preset_size_latent import PresetSizeLatent
from .nodes.load_lora_from_folder import LoadLoraFromFolder

NODE_CLASS_MAPPINGS = {
    "PresetSizeLatent": PresetSizeLatent,
    "LoadLoraFromFolder": LoadLoraFromFolder
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PresetSizeLatent": "🐟Preset Size Latent",
    "LoadLoraFromFolder": "🐟Load LoRA (Folder)"
}

WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

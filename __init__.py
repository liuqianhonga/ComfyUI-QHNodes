from .nodes.preset_size_latent import PresetSizeLatent
from .nodes.load_lora_from_folder import LoadLoraFromFolder
from .submodules_loader import load_submodules
import os

# Set category for main repo nodes
PresetSizeLatent.CATEGORY = "🐟QHNodes"
LoadLoraFromFolder.CATEGORY = "🐟QHNodes"

# Load submodules
submodule_nodes, submodule_display_names = load_submodules(os.path.dirname(__file__))

# Merge all node mappings
NODE_CLASS_MAPPINGS = {
    "PresetSizeLatent": PresetSizeLatent,
    "LoadLoraFromFolder": LoadLoraFromFolder,
    **submodule_nodes
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PresetSizeLatent": "🐟Preset Size Latent",
    "LoadLoraFromFolder": "🐟Load LoRA (Folder)",
    **submodule_display_names
}

# Set web directory
WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

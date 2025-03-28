import os
from .nodes.preset_size_latent import PresetSizeLatent
from .nodes.load_lora_from_folder import LoadLoraFromFolder
from .nodes.sampler_settings import SamplerSettings
from .nodes.gemini import Gemini
from .nodes.json_unpack import JsonUnpack
from .nodes.image_count_from_folder import ImageCountFromFolder
from .nodes.load_image_from_folder import LoadImageFromFolder
from .nodes.file_save import FileSave
from .nodes.unified_prompt_generator import UnifiedPromptGeneratorNode
from .nodes.dynamic_expression import DynamicExpressionNode
from .nodes.load_prompts_from_folder import LoadPromptsFromFolder
from .submodules_loader import load_submodules
from .requirements_installer import ensure_dependencies

# Check and install dependencies on load - only once per session
ensure_dependencies()

# Set category for main repo nodes
PresetSizeLatent.CATEGORY = "🐟QHNodes"
LoadLoraFromFolder.CATEGORY = "🐟QHNodes"
SamplerSettings.CATEGORY = "🐟QHNodes"
Gemini.CATEGORY = "🐟QHNodes"
JsonUnpack.CATEGORY = "🐟QHNodes"
ImageCountFromFolder.CATEGORY = "🐟QHNodes"
LoadImageFromFolder.CATEGORY = "🐟QHNodes"
FileSave.CATEGORY = "🐟QHNodes"
UnifiedPromptGeneratorNode.CATEGORY = "🐟QHNodes"
DynamicExpressionNode.CATEGORY = "🐟QHNodes"
LoadPromptsFromFolder.CATEGORY = "🐟QHNodes"

# Load submodules
submodule_nodes, submodule_display_names = load_submodules(os.path.dirname(__file__))

# Merge all node mappings
NODE_CLASS_MAPPINGS = {
    "PresetSizeLatent": PresetSizeLatent,
    "LoadLoraFromFolder": LoadLoraFromFolder,
    "SamplerSettings": SamplerSettings,
    "Gemini": Gemini,
    "JsonUnpack": JsonUnpack,
    "ImageCountFromFolder": ImageCountFromFolder,
    "LoadImageFromFolder": LoadImageFromFolder,
    "FileSave": FileSave,
    "UnifiedPromptGenerator": UnifiedPromptGeneratorNode,
    "DynamicExpression": DynamicExpressionNode,
    "LoadPromptsFromFolder": LoadPromptsFromFolder,
    **submodule_nodes
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PresetSizeLatent": "🐟Preset Size Latent",
    "LoadLoraFromFolder": "🐟Load LoRA (Folder)",
    "SamplerSettings": "🐟Sampler Settings",
    "Gemini": "🐟Gemini",
    "JsonUnpack": "🐟JSON Unpack",
    "ImageCountFromFolder": "🐟Image Count From Folder",
    "LoadImageFromFolder": "🐟Load Image From Folder",
    "FileSave": "🐟File Save",
    "UnifiedPromptGenerator": "🐟Unified Prompt Generator",
    "DynamicExpression": "🐟Dynamic Expression",
    "LoadPromptsFromFolder": "🐟Load Prompts From Folder",
    **submodule_display_names
}

# Set web directory
WEB_DIRECTORY = "./web"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

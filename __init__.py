from .nodes.preset_size_latent import PresetSizeLatent

NODE_CLASS_MAPPINGS = {
    "PresetSizeLatent": PresetSizeLatent
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PresetSizeLatent": "🐟Preset Size Latent"
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]

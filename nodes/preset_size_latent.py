"""
Preset Size Latent Node
Generate latent with preset sizes for common social media formats and camera aspect ratios
"""
import torch
import json
import os

class PresetSizeLatent:
    """
    Generate latent with preset sizes for common social media formats and camera aspect ratios
    """
    
    @classmethod
    def INPUT_TYPES(s):
        # Load presets from json file
        config_path = os.path.join(os.path.dirname(__file__), "preset_sizes.json")
        presets = []
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Filter out category markers (objects with empty dict as value)
                presets = [k for k, v in data.items() if isinstance(v, list)]
        
        return {
            "required": {
                "use_preset": ("BOOLEAN", {"default": True, "label": "Use Preset"}),
                "preset": (presets, {"default": presets[0] if presets else "手机竖屏 16:9 (Phone Portrait, 1080×1920)"}),
                "width": ("INT", {"default": 1080, "min": 64, "max": 8192, "step": 8, "label": "Width"}),
                "height": ("INT", {"default": 1920, "min": 64, "max": 8192, "step": 8, "label": "Height"}),
                "swap_dimensions": ("BOOLEAN", {"default": False, "label": "Swap Width/Height"}),
                "scale_factor": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1, "label": "Scale Factor"}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 64, "label": "Batch Size"})
            },
        }

    RETURN_TYPES = ("INT", "INT", "LATENT",)
    RETURN_NAMES = ("width", "height", "latent",)
    FUNCTION = "generate"
    CATEGORY = "QHNodes"

    def __init__(self):
        self.presets = {}
        
        # Load presets from json file
        config_path = os.path.join(os.path.dirname(__file__), "preset_sizes.json")
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Filter out category markers
                self.presets = {k: v for k, v in data.items() if isinstance(v, list)}

    def generate(self, use_preset, preset, width, height, swap_dimensions, scale_factor, batch_size):
        # Get dimensions based on preset or custom input
        if use_preset:
            final_width, final_height = self.presets[preset]
        else:
            final_width = width
            final_height = height
        
        if swap_dimensions:
            final_width, final_height = final_height, final_width
            
        # Apply scale factor
        final_width = int(final_width * scale_factor)
        final_height = int(final_height * scale_factor)
        
        # Generate empty latent tensor
        latent = torch.zeros([batch_size, 4, final_height // 8, final_width // 8])
        
        return (final_width, final_height, {"samples": latent})

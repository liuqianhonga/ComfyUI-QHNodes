import comfy.samplers
import comfy.sample
from .lib import ANY

class SamplerSettings:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "sampler_name": (comfy.samplers.KSampler.SAMPLERS, ),
                "scheduler_name": (comfy.samplers.KSampler.SCHEDULERS, ),
                "steps": ("INT", {"default": 30, "min": 1, "max": 100}),
                "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
            },
        }
    
    RETURN_TYPES = (ANY, ANY, "INT", "FLOAT")
    RETURN_NAMES = ("sampler_name", "scheduler_name", "steps", "denoise")
    FUNCTION = "get_sampler"
    CATEGORY = "🐟QHNodes"

    def get_sampler(self, sampler_name, scheduler_name, steps, denoise):
        return (sampler_name, scheduler_name, steps, denoise)

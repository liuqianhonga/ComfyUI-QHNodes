import os
import glob
from .lib import IMAGE_EXTENSIONS

class ImageCountFromFolder:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder": ("STRING", {"default": "", "multiline": False}),
            },
        }

    RETURN_TYPES = ("INT",)
    FUNCTION = "count_images"
    CATEGORY = "🐟QHNodes"

    def count_images(self, folder):
        if not os.path.exists(folder):
            return (0,)
            
        count = 0
        for ext in IMAGE_EXTENSIONS:
            count += len(glob.glob(os.path.join(folder, ext)))
            
        return (count,)

import os
import glob
from PIL import Image
import numpy as np
import torch
import folder_paths
from .lib import IMAGE_EXTENSIONS

class LoadImageFromFolder:
    def __init__(self):
        self.cached_folder = None
        self.cached_files = None
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder": ("STRING", {"default": "", "multiline": False}),
                "start_index": ("INT", {"default": 0, "min": 0, "max": 10000}),
                "load_cap": ("INT", {"default": 1, "min": 1, "max": 100}),
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("images", "image_names", "image_paths")
    OUTPUT_IS_LIST = (True, True, True)
    FUNCTION = "load_images"
    CATEGORY = "🐟QHNodes"

    def get_image_files(self, folder):
        # If we have cached files for this folder, return them
        if self.cached_folder == folder and self.cached_files is not None:
            return self.cached_files
            
        # Get list of image files
        image_files = []
        for ext in IMAGE_EXTENSIONS:
            image_files.extend(glob.glob(os.path.join(folder, ext)))
        
        # Sort files to ensure consistent ordering
        image_files.sort()
        
        # Cache the results
        self.cached_folder = folder
        self.cached_files = image_files
        
        return image_files

    def load_images(self, folder, start_index, load_cap):
        if not os.path.exists(folder):
            return [], [], []
            
        image_files = self.get_image_files(folder)
        
        # Apply start_index and load_cap
        end_index = min(start_index + load_cap, len(image_files))
        selected_files = image_files[start_index:end_index]
        
        images = []
        image_names = []
        image_paths = []
        
        for file_path in selected_files:
            try:
                img = Image.open(file_path)
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                # Convert to numpy array and normalize to float32
                img_array = np.array(img).astype(np.float32) / 255.0
                # Convert to torch tensor with shape [1, H, W, 3]
                image = torch.from_numpy(img_array.copy())[None,]
                images.append(image)
                image_names.append(os.path.basename(file_path))
                image_paths.append(file_path)
            except Exception as e:
                print(f"Error loading image {file_path}: {str(e)}")
                continue
                
        if not images:
            return [], [], []
            
        return (images, image_names, image_paths)

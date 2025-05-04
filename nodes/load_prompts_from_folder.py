import os
import glob
from PIL import Image
import numpy as np
import torch
from .lib import IMAGE_EXTENSIONS

class LoadPromptsFromFolder:
    def __init__(self):
        self.cached_folder = None
        self.cached_files = None
        self.current_index = 0
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "folder": ("STRING", {"default": "", "multiline": False}),
                "file_extension": ("STRING", {"default": ".txt", "multiline": False}),
                "loop_mode": ("BOOLEAN", {"default": False}),
                "start_index": ("INT", {"default": 0, "min": 0, "max": 10000}),
                "load_cap": ("INT", {"default": -1, "min": -1, "max": 100}),
            },
        }

    RETURN_TYPES = ("STRING", "IMAGE", "INT")
    RETURN_NAMES = ("prompts", "images", "current_index")
    OUTPUT_IS_LIST = (True, True, False)
    FUNCTION = "load_prompts"
    CATEGORY = "🐟QHNodes"
    IS_CHANGED = True

    def get_prompt_files(self, folder, file_extension):
        # Return cached files if available
        if self.cached_folder == folder and self.cached_files is not None:
            return self.cached_files
            
        # Get all prompt files
        prompt_files = glob.glob(os.path.join(folder, f"*{file_extension}"))
        
        # Sort files for consistent ordering
        prompt_files.sort()
        
        # Cache the results
        self.cached_folder = folder
        self.cached_files = prompt_files
        
        return prompt_files

    def load_prompts(self, folder, file_extension, loop_mode, start_index, load_cap):
        if not os.path.exists(folder):
            return ([], [], 0)
            
        prompt_files = self.get_prompt_files(folder, file_extension)
        if not prompt_files:
            return ([], [], 0)

        if loop_mode:
            # Use current index in loop mode
            actual_index = self.current_index
            # Update index for next execution
            self.current_index = (self.current_index + 1) % len(prompt_files)
            # Load only one file in loop mode
            selected_files = [prompt_files[actual_index]]
        else:
            # Return all files if load_cap is -1
            if load_cap == -1:
                selected_files = prompt_files[start_index:]
                actual_index = start_index
            else:
                # Use start_index and load_cap in normal mode
                end_index = min(start_index + load_cap, len(prompt_files))
                selected_files = prompt_files[start_index:end_index]
                actual_index = start_index
        
        prompts = []
        images = []
        
        for file_path in selected_files:
            try:
                # Load text prompt
                with open(file_path, 'r', encoding='utf-8') as f:
                    prompt = f.read().strip()
                prompts.append(prompt)
                
                # Try to load corresponding image with the same name but different extension
                base_name = os.path.splitext(file_path)[0]
                image_found = False
                
                # Try all supported image extensions
                for ext in IMAGE_EXTENSIONS:
                    # Remove wildcard from extension pattern
                    ext_clean = ext.replace("*", "")
                    img_path = base_name + ext_clean
                    
                    if os.path.exists(img_path):
                        try:
                            img = Image.open(img_path)
                            # Convert to RGB if necessary
                            if img.mode != 'RGB':
                                img = img.convert('RGB')
                            # Convert to numpy array and normalize to float32
                            img_array = np.array(img).astype(np.float32) / 255.0
                            # Convert to torch tensor with shape [1, H, W, 3]
                            image = torch.from_numpy(img_array.copy())[None,]
                            images.append(image)
                            image_found = True
                            break
                        except Exception as e:
                            print(f"Error loading image {img_path}: {str(e)}")
                            continue
                
                # If no image found, add an empty placeholder
                if not image_found:
                    # Create a small 1x1 black image as placeholder
                    empty_img = torch.zeros(1, 1, 1, 3, dtype=torch.float32)
                    images.append(empty_img)
                    
            except Exception as e:
                print(f"Error loading prompt file {file_path}: {str(e)}")
                continue
                
        return (prompts, images, actual_index) 
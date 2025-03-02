import os
import glob

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

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("prompts", "current_index")
    OUTPUT_IS_LIST = (True, False)
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
            return ([], 0)
            
        prompt_files = self.get_prompt_files(folder, file_extension)
        if not prompt_files:
            return ([], 0)

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
        
        for file_path in selected_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    prompt = f.read().strip()
                prompts.append(prompt)
            except Exception as e:
                print(f"Error loading prompt file {file_path}: {str(e)}")
                continue
                
        return (prompts, actual_index) 
import os
import json
import re

class UnifiedPromptGeneratorNode:
    @classmethod
    def load_options(cls):
        try:
            options_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "unified_prompt_options.json")
            with open(options_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading options: {e}")
            return {}
    
    @staticmethod
    def extract_english(text):
        # Extract the English part before the Chinese characters in parentheses
        match = re.match(r'([^(]+)(?:\([^)]+\))?', text)
        return match.group(1).strip() if match else text

    @classmethod
    def INPUT_TYPES(s):
        options = s.load_options()
        required_inputs = {}
        
        # Convert JSON structure to ComfyUI input format
        for category in options.values():
            for field_name, field_data in category.items():
                choices = field_data["choices"]
                required_inputs[field_name] = (choices, {"default": field_data["default"]})
        
        return {"required": required_inputs} if required_inputs else {
            "required": {
                "message": ("STRING", {"default": "Error: Could not load options"})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)
    FUNCTION = "generate_prompt"
    CATEGORY = "Prompt Generation"

    def generate_prompt(self, **kwargs):
        if "message" in kwargs:
            return (kwargs["message"],)
        
        # Extract English parts from all inputs
        clean_kwargs = {k: self.extract_english(v) for k, v in kwargs.items()}
            
        # Appearance
        appearance_parts = []
        if clean_kwargs['race']:
            appearance_parts.append(clean_kwargs['race'])
        if clean_kwargs['skin']:
            appearance_parts.append(clean_kwargs['skin'])
        if clean_kwargs['hair']:
            appearance_parts.append(clean_kwargs['hair'])
        if clean_kwargs['eyes']:
            appearance_parts.append(clean_kwargs['eyes'])
        if clean_kwargs['lips']:
            appearance_parts.append(clean_kwargs['lips'])
        appearance = f"A young {', '.join(appearance_parts)} person" if appearance_parts else ""

        # Body
        body_parts = []
        if clean_kwargs['body'] and clean_kwargs['body'] != 'none':
            body_parts.append(clean_kwargs['body'])
        body = f"She has {', '.join(body_parts)}" if body_parts else ""

        # OOTD (Outfit of the Day)
        outfit_parts = []
        if clean_kwargs['top'] and clean_kwargs['top'] != 'none':
            outfit_parts.append(clean_kwargs['top'])
        if clean_kwargs['bottom'] and clean_kwargs['bottom'] != 'none':
            outfit_parts.append(clean_kwargs['bottom'])
        if clean_kwargs['shoes'] and clean_kwargs['shoes'] != 'none':
            outfit_parts.append(clean_kwargs['shoes'])
        clothing = f"She is wearing {', '.join(outfit_parts)}" if outfit_parts else ""

        # Pose and Expression
        pose_desc = ""
        pose = clean_kwargs['pose']
        expression = clean_kwargs['expression']
        if pose and expression and pose != 'none' and expression != 'none':
            pose_desc = f"She is {pose} and has a {expression}"
        elif pose and pose != 'none':
            pose_desc = f"She is {pose}"
        elif expression and expression != 'none':
            pose_desc = f"She has a {expression}"

        # Environment
        environment = ""
        scene = clean_kwargs['scene']
        lighting = clean_kwargs['lighting']
        if scene and lighting and scene != 'none' and lighting != 'none':
            environment = f"The image is set in {scene}. The lighting is {lighting}"
        elif scene and scene != 'none':
            environment = f"The image is set in {scene}"
        elif lighting and lighting != 'none':
            environment = f"The lighting is {lighting}"

        # Photography
        photography_parts = []
        
        # Add composition if specified
        if clean_kwargs['composition'] and clean_kwargs['composition'] != 'none':
            photography_parts.append(f"composed with {clean_kwargs['composition']}")
        
        # Add view if specified
        if clean_kwargs['view'] and clean_kwargs['view'] != 'none':
            photography_parts.append(f"taken at {clean_kwargs['view']}")
        
        # Add angle if specified
        if clean_kwargs['angle'] and clean_kwargs['angle'] != 'none':
            photography_parts.append(f"with {clean_kwargs['angle']}")
        
        # Add focus if specified
        if clean_kwargs['focus'] and clean_kwargs['focus'] != 'none':
            photography_parts.append(f"using {clean_kwargs['focus']}")
        
        # Add style as enhancement if specified
        if clean_kwargs['style'] and clean_kwargs['style'] != 'none':
            photography_parts.append(f"enhanced with {clean_kwargs['style']}")
        
        photography = f"The image is {', '.join(photography_parts)}" if photography_parts else ""

        # Combine all sections into a final prompt
        prompt_parts = [p for p in [appearance, body, clothing, pose_desc, environment, photography] if p]

        final_prompt = ". ".join(prompt_parts)
        return (final_prompt,)

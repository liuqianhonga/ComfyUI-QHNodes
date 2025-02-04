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

    def parse_choice(self, choice_str):
        """Parse a choice string in format 'category.style: description(类别.风格：描述)'"""
        if choice_str == "none(无)" or choice_str == "none" or not choice_str:
            return ""
            
        # Extract English part using existing method
        en_part = self.extract_english(choice_str)
        
        # Split category and description
        if ': ' in en_part:
            # Case with full description
            category_style, description = en_part.split(': ', 1)
            # Return only the description part
            return description
        else:
            # Case without description, return the entire English part
            return en_part

    def generate_prompt(self, **kwargs):
        if "message" in kwargs:
            return (kwargs["message"],)
        
        # Use parse_choice instead of extract_english
        clean_kwargs = {k: self.parse_choice(v) for k, v in kwargs.items()}
            
        # Appearance
        appearance_parts = []
        if clean_kwargs['age_gender'] and clean_kwargs['age_gender'] != 'none':
            appearance_parts.append(clean_kwargs['age_gender'])
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
        appearance = f"A {', '.join(appearance_parts)}" if appearance_parts else ""

        # Update pronouns based on gender
        gender = clean_kwargs.get('age_gender', '').lower()
        if 'male' in gender or 'boy' in gender or 'man' in gender:
            pronoun = 'He'
        else:
            pronoun = 'She'  # Default to female pronouns

        # Body
        body_parts = []
        if clean_kwargs['body'] and clean_kwargs['body'] != 'none':
            # Split body description
            body_parts = clean_kwargs['body'].split(': ', 1)
            if len(body_parts) > 1:
                # Use the detailed description after the colon
                body_type, description = body_parts
                body = f"{pronoun} has {description}"
            else:
                # If no colon found, use the entire string
                body = f"{pronoun} has {clean_kwargs['body']}"
        else:
            body = ""

        # OOTD (Outfit of the Day)
        outfit_parts = []
        if clean_kwargs['top'] and clean_kwargs['top'] != 'none':
            outfit_parts.append(clean_kwargs['top'])
        if clean_kwargs['bottom'] and clean_kwargs['bottom'] != 'none':
            outfit_parts.append(clean_kwargs['bottom'])
        if clean_kwargs['shoes'] and clean_kwargs['shoes'] != 'none':
            outfit_parts.append(clean_kwargs['shoes'])
        if clean_kwargs['hat'] and clean_kwargs['hat'] != 'none':
            outfit_parts.append(clean_kwargs['hat'])
        if clean_kwargs['jewelry'] and clean_kwargs['jewelry'] != 'none':
            outfit_parts.append(clean_kwargs['jewelry'])
        if clean_kwargs['glasses'] and clean_kwargs['glasses'] != 'none':
            outfit_parts.append(clean_kwargs['glasses'])
        if clean_kwargs['handbag'] and clean_kwargs['handbag'] != 'none':
            outfit_parts.append(clean_kwargs['handbag'])
        clothing = f"{pronoun} is wearing {', '.join(outfit_parts)}" if outfit_parts else ""

        # Pose and Expression
        pose_desc = ""
        pose = clean_kwargs['pose']
        expression = clean_kwargs['expression']

        if pose and pose != 'none':
            # Split category and description
            pose_parts = pose.split(': ', 1)
            if len(pose_parts) > 1:
                category_name, description = pose_parts
                # Remove category prefix (e.g., "standing.contrapposto")
                category_name = category_name.split('.')[-1]
                pose_desc = f"{pronoun} is {description}"
            else:
                pose_desc = f"{pronoun} is {pose}"

        if expression and expression != 'none':
            if pose_desc:
                pose_desc += f" and has a {expression}"
            else:
                pose_desc = f"{pronoun} has a {expression}"

        # Environment
        environment = ""
        scene_preset = clean_kwargs['scene_preset']
        
        if scene_preset and scene_preset != 'none':
            # Split category and description
            scene_parts = scene_preset.split(': ', 1)
            if len(scene_parts) > 1:
                category_name, descriptions = scene_parts
                # Split scene and lighting descriptions
                scene, lighting = descriptions.split(', ', 1)
                # Remove category prefix (e.g., "commercial_spaces.mall_boutique")
                category_name = category_name.split('.')[-1]
                environment = f"The image is set in {scene}. The lighting is {lighting}"
            else:
                environment = f"The image is set in {scene_preset}"

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

        # Quality
        quality = ""
        if clean_kwargs['quality'] and clean_kwargs['quality'] != 'none':
            quality = clean_kwargs['quality']

        # Combine all sections into a final prompt
        prompt_parts = [p for p in [appearance, body, clothing, pose_desc, environment, photography, quality] if p]

        final_prompt = ". ".join(prompt_parts)
        return (final_prompt,)


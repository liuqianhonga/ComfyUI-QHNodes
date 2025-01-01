import google.generativeai as genai
from PIL import Image
import numpy as np

# Define a class to interact with the Gemini model
class Gemini:
    # List of available Gemini models
    MODELS = [
        "gemini-2.0-flash-exp",
        "gemini-1.5-flash",
        "gemini-1.5-flash-8b",
        "gemini-1.5-pro"
    ]
    
    # Initialize the class with API key and model
    def __init__(self):
        self.api_key = None
        self.model = None
        
    # Define the input types for the process_image function
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": ""}),
                "model": (cls.MODELS, {"default": "gemini-2.0-flash-exp"}),
                "prompt": ("STRING", {"default": "Describe this image"}),
                "temperature": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 2.0, "step": 0.1}),
                "max_output_tokens": ("INT", {"default": 2048, "min": 1, "max": 8192, "step": 1}),
            },
        }

    # Define the return type and function name for the process_image function
    RETURN_TYPES = ("STRING",)
    FUNCTION = "process_image"
    CATEGORY = "🐟QHNodes"

    # Process an image using the Gemini model
    def process_image(self, image, api_key, model, prompt, temperature, max_output_tokens):
        # Check if a valid API key is provided
        if not api_key:
            raise ValueError("Please provide a valid Google API key")

        try:
            # Configure the API with the provided API key
            genai.configure(api_key=api_key)
            
            # Initialize the model if not already done or if the model has changed
            if not self.model or self.model.model_name != model:
                self.model = genai.GenerativeModel(model)

            # Convert the input tensor to a PIL Image
            img = image.unsqueeze(0)
            pil_image = Image.fromarray(np.clip(255.0 * img.cpu().numpy().squeeze(), 0, 255).astype(np.uint8)).convert('RGB')
            
            # Generate a response from the Gemini model
            response = self.model.generate_content(
                [prompt, pil_image], 
                generation_config=genai.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                    response_mime_type="application/json",
                )
            )
            
            # Return the response text
            return (response.text,)
            
        except Exception as e:
            # Raise any exceptions that occur during processing
            raise e

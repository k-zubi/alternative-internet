import os
import io
import re
import base64
import requests
import fal_client
from typing import Dict, Any, Optional, Callable


class ImageGenerator:
    """Handles image generation using fal.ai's API."""
    
    def __init__(self, cache_dir: str = "image_cache"):
        """
        Initialize the image generator.
        
        Args:
            cache_dir: Directory to cache generated images
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def process_image_name(self, image_name: str) -> str:
        """
        Convert image filename to a prompt.
        
        Args:
            image_name: The name of the image file
            
        Returns:
            A prompt suitable for image generation
        """
        # Remove file extension
        name = os.path.splitext(image_name)[0]
        
        # Replace dashes and underscores with spaces
        name = name.replace('-', ' ').replace('_', ' ')
        
        # Clean up extra spaces
        name = re.sub(r'\s+', ' ', name).strip()
        
        # If the prompt is too short, enhance it
        if len(name) < 10:
            name = f"Detailed illustration of {name}"
        
        return name
    
    def generate_image(self, prompt: str, callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Generate an image based on the prompt.
        
        Args:
            prompt: Text prompt for image generation
            callback: Optional callback for progress updates
            
        Returns:
            Dictionary containing the generated image data
        """
        def on_queue_update(update):
            if isinstance(update, fal_client.InProgress) and callback:
                for log in update.logs:
                    callback(log["message"])
            # No-op for other log messages
        
        # Enhance the prompt to generate better images
        enhanced_prompt = f"{prompt}, high quality, detailed"
        print(f"Generating image with prompt: '{enhanced_prompt}'")
        
        # Generate the image
        result = fal_client.subscribe(
            "fal-ai/flux/schnell",
            arguments={
                "prompt": enhanced_prompt
            },
            with_logs=True,
            on_queue_update=on_queue_update,
        )
        
        # The Flux model returns a specific format
        if isinstance(result, dict) and 'images' in result and not isinstance(result['images'], list):
            # If images is not a list, convert it to the expected format
            result['images'] = [result['images']]
        
        return result
    
    def save_image(self, image_data: Dict[str, Any], image_name: str) -> str:
        """
        Save the generated image to the cache directory.
        
        Args:
            image_data: Image data from fal.ai
            image_name: Name to save the image as
            
        Returns:
            Path to the saved image
        """
        # Ensure image name has the right extension
        if not image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_name = f"{image_name}.png"
            
        # Create full path
        image_path = os.path.join(self.cache_dir, image_name)
        
        # Get image content
        try:
            # Check if we have image URLs instead of base64 data
            if isinstance(image_data, dict) and 'images' in image_data and isinstance(image_data['images'], list):
                image_item = image_data['images'][0]
                
                # Case 1: Image URL in a dictionary
                if isinstance(image_item, dict) and 'url' in image_item:
                    image_url = image_item['url']
                    response = requests.get(image_url)
                    response.raise_for_status()  # Ensure we got a valid response
                    image_content = response.content
                
                # Case 2: Base64 string with data URL format
                elif isinstance(image_item, str) and ',' in image_item:
                    image_content = base64.b64decode(image_item.split(',')[1])
                
                # Case 3: Raw base64 string
                elif isinstance(image_item, str):
                    image_content = base64.b64decode(image_item)
                
                else:
                    raise ValueError("Unsupported image format")
            
            # Alternative formats
            elif isinstance(image_data, dict) and 'image' in image_data:
                if isinstance(image_data['image'], str):
                    image_content = base64.b64decode(image_data['image'])
                else:
                    raise ValueError("Unexpected image format")
                    
            else:
                raise ValueError("Failed to extract image data from response")
                
        except Exception as e:
            raise ValueError(f"Failed to process image data: {e}")
        
        # Save to file
        with open(image_path, 'wb') as f:
            f.write(image_content)
            
        return image_path
    
    def get_or_generate_image(self, image_name: str) -> str:
        """
        Get an image from cache or generate it if not available.
        
        Args:
            image_name: Name of the image file
            
        Returns:
            Path to the image file
        """
        # Ensure image name has the right extension if it doesn't have one
        if not os.path.splitext(image_name)[1]:
            image_name = f"{image_name}.png"
            
        # Check if image exists in cache
        image_path = os.path.join(self.cache_dir, image_name)
        if os.path.exists(image_path):
            print(f"Using cached image: {image_path}")
            return image_path
            
        # Generate new image
        prompt = self.process_image_name(image_name)
        print(f"Generating image for: {prompt}")
        
        image_data = self.generate_image(prompt)
        
        # Save and return path
        return self.save_image(image_data, image_name)
        
    def get_image_as_base64(self, image_name: str) -> str:
        """
        Get image as base64-encoded string.
        
        Args:
            image_name: Name of the image
            
        Returns:
            Base64-encoded image data with mime type
        """
        # Get image path
        image_path = self.get_or_generate_image(image_name)
        
        # Read and encode
        with open(image_path, 'rb') as f:
            image_data = f.read()
            
        # Determine mime type
        ext = os.path.splitext(image_path)[1].lower()
        mime_type = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
        
        # Encode to base64
        encoded = base64.b64encode(image_data).decode('utf-8')
        
        return f"data:{mime_type};base64,{encoded}"
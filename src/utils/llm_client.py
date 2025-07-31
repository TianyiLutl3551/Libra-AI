"""
LLM Client Module
Handles all interactions with Azure OpenAI API for text and vision models
"""

import toml
import json
import base64
import pandas as pd
from io import StringIO
from openai import AzureOpenAI
import re


class LLMClient:
    def __init__(self, secrets_file="config/secrets.toml"):
        """Initialize LLM client with Azure OpenAI configuration."""
        self.secrets = toml.load(secrets_file)
        self.openai_config = self.secrets.get("openai", {})
        
        # Azure OpenAI configuration
        self.endpoint = self.openai_config.get("endpoint")
        self.subscription_key = self.openai_config.get("subscription_key")
        self.deployment = self.openai_config.get("deployment", "gpt-4o")
        self.api_version = self.openai_config.get("api_version", "2024-12-01-preview")
        
        # Model names (using deployment name for Azure)
        self.text_model = self.openai_config.get("model_name", "gpt-4o")
        self.vision_model = self.openai_config.get("model_name", "gpt-4o")
        self.system_prompt = self.openai_config.get(
            "system_prompt", 
            "You are a data analysis expert that helps transform and organize Excel data. Always return valid JSON arrays."
        )
        
        if not self.endpoint or not self.subscription_key:
            raise ValueError("Azure OpenAI endpoint or subscription key not found in secrets file")
        
        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.subscription_key,
            api_version=self.api_version
        )
    
    def process_text(self, prompt: str) -> dict:
        """
        Process text prompt and return structured data.
        
        Args:
            prompt: Text prompt for the LLM
            
        Returns:
            Dictionary with 'table' key containing CSV string
        """
        try:
            response = self.client.chat.completions.create(
                model=self.deployment,  # Use deployment name for Azure
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response.choices[0].message.content.strip()
            print(f"[DEBUG] Raw LLM response:\n{content}")
            
            return self._extract_json_to_csv(content)
            
        except Exception as e:
            print(f"Error calling Azure OpenAI text model: {e}")
            return {"table": ""}
    
    def process_vision(self, image_path: str, prompt: str = None) -> str:
        """
        Process image with vision model for classification.
        
        Args:
            image_path: Path to the image file
            prompt: Custom prompt (optional)
            
        Returns:
            Classification result as string
        """
        if prompt is None:
            prompt = "Classify this picture: is it a blue table or a red table. Return blue or red. Don't return anything else."
        
        try:
            # Read and encode image
            with open(image_path, "rb") as f:
                image_bytes = f.read()
            base64_image = base64.b64encode(image_bytes).decode('utf-8')
            
            response = self.client.chat.completions.create(
                model=self.deployment,  # Use deployment name for Azure
                messages=[
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                    ]}
                ]
            )
            
            content = response.choices[0].message.content.strip().lower()
            
            # Extract classification
            if "blue" in content:
                return "blue"
            elif "red" in content:
                return "red"
            else:
                print(f"Vision model returned unexpected content: {content}")
                return "unknown"
                
        except Exception as e:
            print(f"Error calling Azure OpenAI vision model: {e}")
            return "unknown"
    
    def _extract_json_to_csv(self, content: str) -> dict:
        """
        Extract JSON array from LLM response and convert to CSV.
        
        Args:
            content: Raw LLM response content
            
        Returns:
            Dictionary with 'table' key containing CSV string
        """
        # Use robust JSON extraction method
        json_match = re.search(r'(\[.*?\])', content, re.DOTALL)
        
        if json_match:
            json_str = json_match.group(1)
            try:
                data = json.loads(json_str)
                if not isinstance(data, list):
                    print("LLM response is not a JSON array")
                    return {"table": ""}
                
                # Convert JSON array to CSV format
                df = pd.DataFrame(data)
                csv_buffer = StringIO()
                df.to_csv(csv_buffer, index=False)
                csv_string = csv_buffer.getvalue()
                
                return {"table": csv_string.strip()}
                
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e}")
                return {"table": ""}
        else:
            print("No JSON array found in LLM response.")
            return {"table": ""}


# Global instance for backward compatibility
_llm_client = None

def get_llm_client():
    """Get global LLM client instance."""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client

def real_llm_func(prompt: str) -> dict:
    """Backward compatibility function for text processing."""
    return get_llm_client().process_text(prompt)

def real_llm_vision_func(image_path: str) -> str:
    """Backward compatibility function for vision processing."""
    return get_llm_client().process_vision(image_path) 
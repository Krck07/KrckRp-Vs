"""
LLM Client - Manages HTTP calls to local Vulkan KoboldCpp instances.
Routes prompts to the ~14B Narrator (streaming) or the ~3B Extractor/Assistant.
"""

import httpx
import json
from typing import Dict, Any

class LLMClient:
    def __init__(self):
        # Configure endpoints for different models
        self.narrator_endpoint = "http://localhost:5000"  # Narrator model endpoint
        self.extractor_endpoint = "http://localhost:5001"  # Extractor model endpoint
        self.assistant_endpoint = "http://localhost:5002"  # Assistant model endpoint

    async def call_narrator(self, prompt: str, streaming: bool = True) -> Dict[str, Any]:
        """
        Send prompt to narrator LLM.

        Args:
            prompt: The prompt to send
            streaming: Whether to stream response

        Returns:
            Response from the narrator model
        """
        try:
            async with httpx.AsyncClient() as client:
                data = {
                    "prompt": prompt,
                    "stream": streaming,
                    "max_tokens": 500,  # Reasonable default for narration
                    "temperature": 0.7   # Creative but not too chaotic
                }

                response = await client.post(
                    f"{self.narrator_endpoint}/api/v1/generate",
                    json=data,
                    timeout=30.0
                )

                if response.status_code == 200:
                    result = response.json()
                    return {
                        "text": result.get("results", [{}])[0].get("text", ""),
                        "status": "success"
                    }
                else:
                    return {"error": f"HTTP {response.status_code}: {response.text}", "status": "error"}
        except Exception as e:
            return {"error": str(e), "status": "error"}

    async def call_extractor(self, context: str, player_input: str) -> Dict[str, Any]:
        """
        Send context to extractor LLM for structured output.

        Args:
            context: The narration text
            player_input: Player's input

        Returns:
            Structured JSON from the extractor
        """
        try:
            async with httpx.AsyncClient() as client:
                # Create a prompt that guides the extractor toward schema-constrained output
                prompt = f"""
You are an expert at extracting structured information from narrative text.
From the following narration and player input, identify any canonical changes to game state.

Player Input: {player_input}

Narration: {context}

Respond with ONLY valid JSON matching this schema:
{{"changes": [{{"entity_type": "character|item|location|relationship|quest|faction", "action": "create|modify|delete", "details": {{}}}}]}}
                """

                data = {
                    "prompt": prompt,
                    "max_tokens": 1000,
                    "temperature": 0.2,  # Low temperature for consistent output
                    "grammar": "json"    # Use grammar-constrained generation if supported
                }

                response = await client.post(
                    f"{self.extractor_endpoint}/api/v1/generate",
                    json=data,
                    timeout=30.0
                )

                if response.status_code == 200:
                    result = response.json()
                    text_response = result.get("results", [{}])[0].get("text", "")

                    # Try to parse the JSON from the response
                    try:
                        # Extract JSON from potentially messy output (in case LLM includes other text)
                        start_idx = text_response.find('{')
                        end_idx = text_response.rfind('}') + 1

                        if start_idx != -1 and end_idx != -1:
                            json_str = text_response[start_idx:end_idx]
                            parsed_json = json.loads(json_str)
                            return {"changes": parsed_json.get("changes", []), "status": "success"}
                        else:
                            # If no JSON found, try to extract just the changes part from the response
                            # This is a fallback approach for when the LLM output is slightly malformed
                            if '"changes"' in text_response:
                                start_changes = text_response.find('"changes"')
                                end_changes = text_response.rfind('}') + 1
                                if start_changes != -1 and end_changes != -1:
                                    changes_json = text_response[start_changes:end_changes]
                                    try:
                                        parsed_changes = json.loads(changes_json)
                                        return {"changes": parsed_changes.get("changes", []), "status": "success"}
                                    except Exception:
                                        pass  # Fall through to error handling
                            return {"error": "No valid JSON found in extractor response", "status": "error"}
                    except Exception as e:
                        return {"error": f"Failed to parse JSON: {str(e)}", "status": "error"}
                else:
                    return {"error": f"HTTP {response.status_code}: {response.text}", "status": "error"}
        except Exception as e:
            return {"error": str(e), "status": "error"}

    async def call_assistant(self, request: str) -> Dict[str, Any]:
        """
        Send request to assistant LLM for correction.

        Args:
            request: Plain language correction request

        Returns:
            Response from the assistant
        """
        try:
            async with httpx.AsyncClient() as client:
                prompt = f"""
You are an expert assistant helping fix issues in a role-playing game.
The player has requested the following correction: {request}

Respond only with your best interpretation of what should be corrected and how.
Do not add any extra commentary - just provide a clear, actionable response.
                """

                data = {
                    "prompt": prompt,
                    "max_tokens": 300,
                    "temperature": 0.5
                }

                response = await client.post(
                    f"{self.assistant_endpoint}/api/v1/generate",
                    json=data,
                    timeout=30.0
                )

                if response.status_code == 200:
                    result = response.json()
                    return {
                        "response": result.get("results", [{}])[0].get("text", ""),
                        "status": "success"
                    }
                else:
                    return {"error": f"HTTP {response.status_code}: {response.text}", "status": "error"}
        except Exception as e:
            return {"error": str(e), "status": "error"}

# Example usage
async def get_narration(prompt):
    client = LLMClient()
    return await client.call_narrator(prompt)
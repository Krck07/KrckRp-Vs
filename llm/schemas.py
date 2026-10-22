"""
LLM Schemas - Stores the strict JSON-schema definitions used by:
- Extractor to propose state changes  
- Assistant for correction tools
"""

from typing import List, Dict, Any

# Schema definitions for Extractor output (JSON constrained)
EXTRACTOR_SCHEMA = {
    "type": "object",
    "properties": {
        "changes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "entity_type": {"type": "string", "enum": ["character", "item", "location", "relationship", "quest"]},
                    "action": {"type": "string", "enum": ["create", "modify", "delete"]},
                    "details": {"type": "object"}
                },
                "required": ["entity_type", "action", "details"]
            }
        }
    },
    "required": ["changes"]
}

# Schema for Assistant correction tools
ASSISTANT_TOOL_SCHEMA = {
    "type": "object",
    "properties": {
        "tool_name": {"type": "string"},
        "parameters": {"type": "object"}
    },
    "required": ["tool_name", "parameters"]
}

# Additional schemas would be defined here based on full requirements
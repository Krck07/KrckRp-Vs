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
                    "entity_type": {"type": "string", "enum": ["character", "item", "location", "relationship", "quest", "faction"]},
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

# More detailed schemas based on KrckRP requirements
CHARACTER_CHANGE_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "stats": {"type": "object"},
        "inventory": {"type": "array", "items": {"type": "string"}},
        "location": {"type": "string"},
        "relationships": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "target": {"type": "string"},
                "attitude": {"type": "number"},
                "tags": {"type": "array", "items": {"type": "string"}}
            }
        }}
    },
    "required": ["name"]
}

ITEM_CHANGE_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "location": {"type": "string"},
        "owner": {"type": "string"}
    },
    "required": ["name"]
}

LOCATION_CHANGE_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "connections": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "target": {"type": "string"},
                "distance": {"type": "number"}
            }
        }}
    },
    "required": ["name"]
}

RELATIONSHIP_CHANGE_SCHEMA = {
    "type": "object",
    "properties": {
        "source": {"type": "string"},
        "target": {"type": "string"},
        "attitude": {"type": "number"},
        "tags": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["source", "target"]
}

QUEST_CHANGE_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "summary": {"type": "string"},
        "giver": {"type": "string"},
        "location": {"type": "string"},
        "objectives": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "description": {"type": "string"},
                "status": {"type": "string", "enum": ["proposed", "active", "completed", "failed"]}
            }
        }},
        "state": {"type": "string", "enum": ["proposed", "active", "completed", "failed", "abandoned", "expired"]},
        "origin_turn": {"type": "number"}
    },
    "required": ["title"]
}

FACTION_CHANGE_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "goals": {"type": "array", "items": {"type": "string"}},
        "relationships": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "target": {"type": "string"},
                "attitude": {"type": "number"}
            }
        }}
    },
    "required": ["name"]
}

# Complete schema for extractor changes with detailed structure
DETAILED_EXTRACTOR_SCHEMA = {
    "type": "object",
    "properties": {
        "changes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "entity_type": {"type": "string", "enum": ["character", "item", "location", "relationship", "quest", "faction"]},
                    "action": {"type": "string", "enum": ["create", "modify", "delete"]},
                    "details": {"type": "object"}
                },
                "required": ["entity_type", "action", "details"]
            }
        }
    },
    "required": ["changes"]
}
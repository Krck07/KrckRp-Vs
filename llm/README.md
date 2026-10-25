# LLM Module

This module handles all communication with the local language models used by KrckRP. It provides clients for three different types of models:

1. **Narrator Model** (~14B parameters) - Generates narrative prose and dialogue
2. **Extractor Model** (~3B parameters) - Parses narrations to extract structured state changes  
3. **Assistant Model** - Handles correction requests from players

## Architecture

The LLM module works as a bridge between the KrckRP engine and the local KoboldCpp instances running on localhost:

```
KrckRP Engine ←→ HTTP API → Local KoboldCpp Instances
        ↑
    (LLM Client)
```

Each model runs on its own port:
- Narrator: `http://localhost:5000` 
- Extractor: `http://localhost:5001`
- Assistant: `http://localhost:5002`

## Key Components

### LLMClient Class
The main interface for making calls to the language models. Methods include:
- `call_narrator(prompt, streaming=True)`: Generate narrative text
- `call_extractor(context, player_input)`: Extract structured changes from narration  
- `call_assistant(request)`: Process plain-language correction requests

### Schemas
JSON schemas defining expected input/output formats for the LLMs to ensure consistent parsing and validation.
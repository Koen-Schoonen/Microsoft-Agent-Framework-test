# Microsoft Agent Framework starter

This folder contains a minimal Python agent scaffold built with the Microsoft Agent Framework.

## What it includes

- A model client configured for Ollama
- A small `Agent` object with instructions
- A simple REPL loop for sending user prompts
- Comments that explain the important concepts for learning

## Quick start

1. Install dependencies:
   `py -m pip install -r requirements.txt`
2. Start Ollama locally, or sign in to the Ollama cloud flow.
3. Copy `.env.example` to `.env` and adjust the settings.
4. Run the app:
   `py agent_framework_demo/main.py`

## Model setup ideas

The default is now `OLLAMA_MODEL=gemma4:cloud` because it avoids the common "model not found" issue on smaller machines.

- Local model example: `OLLAMA_MODEL=gemma4:e2b`
- Cloud model example: `OLLAMA_MODEL=gemma4:cloud`

If you use a local model, run:

```bash
ollama pull gemma4:e2b
```

If you use a signed-in cloud model, run:

```bash
ollama signin
```

## Next ideas

- Add a tool such as a calculator or weather lookup
- Add a memory layer or conversation history
- Split logic into separate modules for tools and workflows

This starter is intentionally small so you can grow it without fighting the framework.

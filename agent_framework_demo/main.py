"""Console entrypoint for the sample Microsoft Agent Framework app.

Run this script to chat with the agent from your terminal. It is intentionally
simple so you can modify it as a learning exercise.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

# When this file is run directly (for example: python agent_framework_demo/main.py),
# Python puts the package directory itself on sys.path, not the parent project root.
# That prevents imports like "agent_framework_demo.agent_builder" from working.
# Adding the parent directory keeps both direct execution and module execution working.
if __package__ in (None, ""):
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from agent_framework_demo.agent_builder import ask_agent, create_agent


async def interactive_loop() -> None:
    """A simple REPL loop.

    This is a good starting point for learning:
    - create the agent once
    - loop until the user types exit
    - send each user prompt through the agent
    """
    agent = create_agent()

    print("Microsoft Agent Framework expert assistant")
    print("Ask about agent design, tools, architecture, or Microsoft Learn references.")
    print("Type 'exit' or 'quit' to leave.")
    print("---")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        response = await ask_agent(agent, user_input)
        print(f"Assistant: {response}\n")


if __name__ == "__main__":
    asyncio.run(interactive_loop())

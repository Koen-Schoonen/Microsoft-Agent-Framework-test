"""Build a specialized agent for Q&A and agent-design guidance.

This version is still deliberately approachable for learning, but it behaves more
like an expert assistant. The goal is to help with:
- Microsoft Agent Framework concepts and patterns
- tool design and agent architecture decisions
- local model configuration with Ollama
- practical guidance for Azure / AI platform integration

The design keeps environment setup in one place and the app loop separate, so it
is easy to learn from and extend.
"""

from __future__ import annotations

import os
from typing import Any

from dotenv import load_dotenv
from agent_framework import Agent, Message
from agent_framework.ollama import OllamaChatClient

from agent_framework_demo.knowledge import find_knowledge
from agent_framework_demo.skills import (
    create_document_skill,
    create_flowchart_skill,
)

MAX_CONVERSATION_HISTORY = 5

# Load .env values if present (for example: OLLAMA_HOST, OLLAMA_MODEL)
load_dotenv()


def get_microsoft_learn_references(topic: str) -> str:
    """Return a curated Microsoft Learn reference list for a topic.

    This function is exposed as a tool so the assistant can cite relevant Learn
    sources when answering architecture or framework questions.
    """
    return find_knowledge(topic, max_results=3)


def suggest_agent_architecture(use_case: str, environment: str = "Python") -> str:
    """Turn a business problem into a practical agent architecture.

    The return value is intentionally opinionated but simple enough to be used in
    learning settings. It is meant to encourage real design thinking rather than
    a one-size-fits-all answer.
    """
    use_case = (use_case or "general internal productivity agent").strip()
    environment = environment or "Python"

    overview = [
        "Recommended design:",
        f"- Primary goal: {use_case}",
        f"- Runtime: {environment}",
        "- Keep a model layer, tool layer, and governance layer separate.",
        "- Start with a narrow scope, a single user story, and a measurable success metric.",
    ]

    if "technical" in use_case.lower() or "developer" in use_case.lower():
        overview.append(
            "- Prefer a tool-rich architecture with developer documentation and safe shell/file access only when needed.")
    else:
        overview.append(
            "- Prefer a knowledge layer, secure tool routing, and human approval for sensitive actions.")

    overview.extend([
        "- Add evaluation checks for tool use, hallucination, and edge-case prompts.",
        "- Add logging, tracing, permission checks, and a review loop before production rollout.",
        "- Keep a fallback path for unsupported tasks instead of letting the agent guess.",
    ])
    return "\n".join(overview)


def summarize_agent_framework_basics(topic: str = "agent framework") -> str:
    """Give a compact, practical explanation of the Agent Framework core ideas."""
    topic = (topic or "agent framework").strip().lower()
    return (
        f"The core idea behind the {topic} is to combine a model, a set of tools, and structured instructions "
        "into a predictable run loop. In practice, a small agent usually contains: a model client, a system prompt, "
        "tool definitions, a message loop, and evaluation/guardrail checks. Keep the first version focused and make "
        "the tool boundaries explicit before adding wider enterprise features."
    )


def build_client() -> OllamaChatClient:
    """Create the model client.

    This starter prefers the signed-in Ollama cloud model by default because it is
    the most reliable choice on a smaller machine. If you want to run purely
    locally, set OLLAMA_MODEL=gemma4:e2b and make sure the model is downloaded.

    Local example:
        OLLAMA_HOST=http://localhost:11434
        OLLAMA_MODEL=gemma4:e2b

    Cloud example (when using the signed-in Ollama experience):
        OLLAMA_HOST=http://localhost:11434
        OLLAMA_MODEL=gemma4:cloud
    """
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "gemma4:cloud")
    return OllamaChatClient(host=host, model=model)


def build_agent_tools() -> list[Any]:
    """Return a small tool set for a learning-focused, expert agent.

    This keeps the assistant practical: it can look up Microsoft Learn references,
    suggest agent architecture, explain the framework in plain language, and create
    reusable template-driven outputs for documents and flowcharts.
    """
    return [
        get_microsoft_learn_references,
        suggest_agent_architecture,
        summarize_agent_framework_basics,
        create_document_skill,
        create_flowchart_skill,
    ]


def create_agent() -> Agent:
    """Build an expert assistant using the Ollama chat client and a curated tool set."""
    client = build_client()
    agent = Agent(
        client=client,
        name="agent_framework_expert",
        description="A Q&A assistant focused on building agents with the Microsoft Agent Framework.",
        instructions=(
            "You are a practical expert on Microsoft Agent Framework and agent design. "
            "Answer in a Q&A style, keep responses concise but useful, and favor concrete architecture advice. "
            "When asked for documentation or references, use the knowledge tools to surface the best Microsoft Learn sources. "
            "When asked for a solution design, explain trade-offs, guardrails, evaluation, and deployment in a clear sequence. "
            "When the user wants a reusable output in a standard house style, prefer the document or flowchart skill helpers instead of ad hoc formatting. "
            "If a task is ambiguous, ask a clarifying question before proposing a full design."
        ),
        tools=build_agent_tools(),
    )
    setattr(agent, "conversation_history", [])
    return agent


async def ask_agent(agent: Agent, prompt: str) -> str:
    """Send a user message to the agent and return a plain text response.

    The exact response structure varies across model clients. This helper keeps the
    starter practical by unwrapping the latest message contents when present.
    """
    history = list(getattr(agent, "conversation_history", []))
    conversation_messages: list[Message] = []

    for previous_turn in history[-MAX_CONVERSATION_HISTORY:]:
        conversation_messages.append(
            Message(role="user", contents=[previous_turn["prompt"]]))
        conversation_messages.append(
            Message(role="assistant", contents=[previous_turn["response"]]))

    conversation_messages.append(Message(role="user", contents=[prompt]))

    try:
        response = await agent.run(conversation_messages)
    except Exception as exc:  # pragma: no cover - runtime integration path
        model_name = os.getenv("OLLAMA_MODEL", "gemma4:cloud")
        raise RuntimeError(
            "The agent could not reach the configured Ollama model. "
            f"Current model: {model_name}. "
            "If you want a local model, run 'ollama pull gemma4:e2b' or set "
            "OLLAMA_MODEL=gemma4:e2b. If you want the cloud model, run "
            "'ollama signin' and make sure the model is available."
        ) from exc

    # The exact structure of the response depends on the model/client. This
    # defensive unwrapping makes the starter friendlier for learning and tweaking.
    answer = str(response)
    if hasattr(response, "messages") and response.messages:
        last_message = response.messages[-1]
        if hasattr(last_message, "contents") and last_message.contents:
            first_content = last_message.contents[0]
            if hasattr(first_content, "text"):
                answer = first_content.text
            elif isinstance(first_content, str):
                answer = first_content

    history.append({"prompt": prompt, "response": answer})
    if len(history) > MAX_CONVERSATION_HISTORY:
        history = history[-MAX_CONVERSATION_HISTORY:]
    setattr(agent, "conversation_history", history)
    return answer

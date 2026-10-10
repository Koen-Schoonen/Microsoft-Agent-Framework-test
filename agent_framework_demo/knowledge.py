"""Curated knowledge snippets for a Microsoft Agent Framework expert assistant.

This small knowledge base is intentionally easy to extend. It is meant to be a
lightweight, learning-friendly layer that can later evolve into a richer retrieval
system backed by local docs, SharePoint, Azure AI Search, or Microsoft Learn pages.
"""

from __future__ import annotations

MICROSOFT_LEARN_SOURCES = [
    {
        "title": "Microsoft Agent Framework overview",
        "url": "https://learn.microsoft.com/azure/ai-foundry/agents/overview",
        "summary": "High-level overview of agent patterns, tools, memory, orchestration, and hosted runtimes.",
    },
    {
        "title": "Build agents with Azure AI Foundry",
        "url": "https://learn.microsoft.com/azure/ai-foundry/agents/quickstart",
        "summary": "Quickstart guidance for setting up agent experiences, connecting model and tools, and getting started safely.",
    },
    {
        "title": "Azure AI Agents Python SDK",
        "url": "https://learn.microsoft.com/python/api/overview/azure/ai-agents-readme?view=azure-python",
        "summary": "Python library reference and conceptual guidance for agent runtime patterns and client usage.",
    },
    {
        "title": "Microsoft Learn AI fundamentals",
        "url": "https://learn.microsoft.com/training/browse/?products=azure-ai-foundry",
        "summary": "Training and architecture material for Azure AI and agentic application patterns.",
    },
    {
        "title": "Responsible AI and governance",
        "url": "https://learn.microsoft.com/azure/ai-services/responsible-ai-overview",
        "summary": "Guidance on evaluation, safety, governance, and operational controls for AI applications.",
    },
]


def find_knowledge(query: str, max_results: int = 3) -> str:
    """Return the best matching curated Microsoft Learn references for a topic.

    This is intentionally simple but useful as a teaching aid. The model can use
    this tool when a user asks for guidance, references, or architecture ideas
    related to Microsoft Agent Framework and agent design.
    """
    normalized_query = (query or "").strip().lower()
    if not normalized_query:
        return "No query provided. Please ask about a Microsoft Agent Framework topic, architecture pattern, or deployment concern."

    scored_matches: list[tuple[int, dict[str, str]]] = []
    for source in MICROSOFT_LEARN_SOURCES:
        haystack = " ".join(
            [
                source.get("title", ""),
                source.get("summary", ""),
                source.get("url", ""),
            ]
        ).lower()
        score = sum(1 for term in normalized_query.split() if term in haystack)
        if score:
            scored_matches.append((score, source))

    if not scored_matches:
        return (
            "No exact match was found in the curated Microsoft Learn index. "
            "Try a broader question about agent architecture, tool calling, model selection, "
            "or Azure AI Foundry guidance."
        )

    ranked = sorted(scored_matches, key=lambda item: item[0], reverse=True)[
        :max_results]
    lines = ["Recommended Microsoft Learn references:"]
    for _, source in ranked:
        lines.append(f"- {source['title']}: {source['url']}")
        lines.append(f"  Why this helps: {source['summary']}")
    return "\n".join(lines)

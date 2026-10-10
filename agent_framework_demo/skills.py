"""Skill-style helpers for template-driven agent workflows.

These are not separate Agent Framework runtime primitives. They are higher-level
skill wrappers that orchestrate a consistent output format for useful document and
visualization tasks. The pattern is:

- generic tools do the low-level work
- a skill enforces template rules and house style
- the agent can call the skill as a normal Python callable tool
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from docx import Document


@dataclass
class DocumentTemplate:
    title: str
    subtitle: str = ""
    sections: list[str] | None = None
    footer: str = "Confidential"


@dataclass
class FlowchartTemplate:
    title: str
    node_fill: str = "#D9EAF7"
    edge_color: str = "#3A5F8A"
    font_family: str = "Segoe UI"
    layout: str = "top-down"
    padding: int = 30


def _ensure_document_template(document: DocumentTemplate | dict[str, Any]) -> DocumentTemplate:
    if isinstance(document, dict):
        return DocumentTemplate(
            title=document.get("title", "Untitled document"),
            subtitle=document.get("subtitle", ""),
            sections=document.get("sections") or [
                "Overview", "Details", "Next steps"],
            footer=document.get("footer", "Confidential"),
        )
    return document


def _ensure_flowchart_template(flow: FlowchartTemplate | dict[str, Any]) -> FlowchartTemplate:
    if isinstance(flow, dict):
        return FlowchartTemplate(
            title=flow.get("title", "Process flow"),
            node_fill=flow.get("node_fill", "#D9EAF7"),
            edge_color=flow.get("edge_color", "#3A5F8A"),
            font_family=flow.get("font_family", "Segoe UI"),
            layout=flow.get("layout", "top-down"),
            padding=flow.get("padding", 30),
        )
    return flow


def generate_docx_template(document: DocumentTemplate | dict[str, Any], output_path: str | None = None) -> str:
    """Generate a DOCX with a consistent corporate house style and return the saved path."""
    document = _ensure_document_template(document)
    doc = Document()

    doc.styles["Normal"].font.name = "Segoe UI"
    doc.styles["Normal"].font.size = 11
    doc.styles["Normal"].paragraph_format.space_after = 6

    header = doc.add_heading(document.title, level=1)
    header.alignment = 1
    if document.subtitle:
        p = doc.add_paragraph(document.subtitle)
        p.italic = True

    for section in document.sections or ["Overview", "Details", "Next steps"]:
        doc.add_heading(section, level=2)
        doc.add_paragraph(
            "This section follows the standard corporate template and can be replaced with your content.")

    doc.add_paragraph()
    doc.add_paragraph(f"Confidentiality: {document.footer}")

    if output_path is None:
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), ".."))
        output_path = os.path.join(project_root, "generated_document.docx")

    doc.save(output_path)
    return output_path


def generate_flowchart_template(flow: FlowchartTemplate | dict[str, Any], output_path: str | None = None) -> str:
    """Generate a Mermaid flowchart in a consistent company style and return the saved path."""
    flow = _ensure_flowchart_template(flow)
    if output_path is None:
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), ".."))
        output_path = os.path.join(project_root, "generated_flowchart.md")

    mermaid = [
        "```mermaid",
        "flowchart " + ("TB" if flow.layout == "top-down" else "LR"),
        f"A[Start]-->|Begin|B[{flow.title}]",
        "B --> C{Review}",
        "C --> D[Action]",
        "D --> E[Result]",
        "style A fill:{flow.node_fill},stroke:{flow.edge_color},stroke-width:2px,color:#1F1F1F",
        "style B fill:{flow.node_fill},stroke:{flow.edge_color},stroke-width:2px,color:#1F1F1F",
        "style C fill:{flow.node_fill},stroke:{flow.edge_color},stroke-width:2px,color:#1F1F1F",
        "style D fill:{flow.node_fill},stroke:{flow.edge_color},stroke-width:2px,color:#1F1F1F",
        "style E fill:{flow.node_fill},stroke:{flow.edge_color},stroke-width:2px,color:#1F1F1F",
        "linkStyle default stroke:{flow.edge_color},stroke-width:2px",
        "classDef default font-family:'{flow.font_family}',font-size:12px",
        "```",
    ]

    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(mermaid))

    return output_path


def create_document_skill(title: str, subtitle: str = "", sections: list[str] | None = None) -> str:
    """Create a DOCX in a standard corporate template and return the file path."""
    template = DocumentTemplate(
        title=title,
        subtitle=subtitle,
        sections=sections or ["Overview", "Details", "Next steps"],
    )
    return generate_docx_template(template)


def create_flowchart_skill(title: str, layout: str = "top-down") -> str:
    """Create a diagram in a corporate house style and return the saved file path."""
    template = FlowchartTemplate(title=title, layout=layout)
    return generate_flowchart_template(template)

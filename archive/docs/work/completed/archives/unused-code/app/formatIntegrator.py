"""Format integration for unified markdown, HTML, and JSON output."""

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class FormatConfig:
    """Configuration for format conversion."""

    includeToc: bool = True
    prettifyJson: bool = True
    htmlTemplate: Optional[str] = None
    jsonIndent: int = 2


class FormatIntegrator:
    """Integrate and convert between multiple documentation formats."""

    def __init__(self, config: Optional[FormatConfig] = None):
        """Initialize format integrator with configuration."""
        self.config = config or FormatConfig()
        self._formats = {}

    def registerFormat(self, name: str, handler: Any) -> None:
        """Register a format handler."""
        self._formats[name] = handler

    def getRegisteredFormats(self) -> List[str]:
        """Get list of registered format names."""
        return list(self._formats.keys())

    def markdownToHtml(self, markdown: str) -> str:
        """Convert markdown to HTML."""
        if not markdown:
            return ""
        lines = markdown.split("\n")
        html = []
        for line in lines:
            if line.startswith("# "):
                html.append(f"<h1>{line[2:]}</h1>")
            elif line.startswith("## "):
                html.append(f"<h2>{line[3:]}</h2>")
            elif line.startswith("### "):
                html.append(f"<h3>{line[4:]}</h3>")
            elif line.startswith("- ") or line.startswith("* "):
                html.append(f"<li>{line[2:]}</li>")
            elif line.startswith("`"):
                html.append(f"<code>{line}</code>")
            elif line.startswith("**"):
                text = line.replace("**", "<strong>").replace("**", "</strong>")
                html.append(f"<p>{text}</p>")
            elif line.strip():
                html.append(f"<p>{line}</p>")
        return "\n".join(html)

    def markdownToJson(self, markdown: str, title: str = "Document") -> str:
        """Convert markdown to JSON."""
        if not markdown:
            return json.dumps({"title": title, "content": ""}, indent=self.config.jsonIndent)
        lines = markdown.split("\n")
        sections = []
        currentSection = None
        for line in lines:
            if line.startswith("# "):
                if currentSection:
                    sections.append(currentSection)
                currentSection = {"heading": line[2:], "level": 1, "content": []}
            elif line.startswith("## "):
                if currentSection:
                    sections.append(currentSection)
                currentSection = {"heading": line[3:], "level": 2, "content": []}
            elif line.strip():
                if currentSection is None:
                    currentSection = {"heading": "Content", "level": 1, "content": []}
                currentSection["content"].append(line)
        if currentSection:
            sections.append(currentSection)
        output = {"title": title, "sections": sections}
        return json.dumps(
            output, indent=self.config.jsonIndent if self.config.prettifyJson else None
        )

    def jsonToMarkdown(self, jsonContent: str) -> str:
        """Convert JSON to markdown."""
        try:
            data = json.loads(jsonContent)
        except json.JSONDecodeError:
            return ""
        lines = []
        if "title" in data:
            lines.append(f"# {data['title']}")
            lines.append("")
        if "sections" in data:
            for section in data["sections"]:
                level = section.get("level", 1)
                heading = "#" * level
                lines.append(f"{heading} {section.get('heading', '')}")
                lines.append("")
                for content in section.get("content", []):
                    lines.append(content)
                lines.append("")
        elif "content" in data:
            lines.append(data["content"])
        return "\n".join(lines)

    def jsonToHtml(self, jsonContent: str) -> str:
        """Convert JSON to HTML."""
        markdown = self.jsonToMarkdown(jsonContent)
        return self.markdownToHtml(markdown)

    def htmlToMarkdown(self, html: str) -> str:
        """Convert HTML back to markdown (basic)."""
        if not html:
            return ""
        # Simple HTML to markdown conversion
        text = html
        text = text.replace("<h1>", "# ").replace("</h1>", "")
        text = text.replace("<h2>", "## ").replace("</h2>", "")
        text = text.replace("<h3>", "### ").replace("</h3>", "")
        text = text.replace("<strong>", "**").replace("</strong>", "**")
        text = text.replace("<em>", "*").replace("</em>", "*")
        text = text.replace("<li>", "- ").replace("</li>", "")
        text = text.replace("<p>", "").replace("</p>", "\n")
        text = text.replace("<code>", "`").replace("</code>", "`")
        return text

    def generateTableOfContents(self, markdown: str) -> str:
        """Generate table of contents from markdown."""
        lines = markdown.split("\n")
        toc = ["## Table of Contents\n"]
        for line in lines:
            if line.startswith("# "):
                continue  # Skip main title
            elif line.startswith("## "):
                heading = line[3:].strip()
                toc.append(f"- [{heading}](#{heading.lower().replace(' ', '-')})")
            elif line.startswith("### "):
                heading = line[4:].strip()
                toc.append(f"  - [{heading}](#{heading.lower().replace(' ', '-')})")
        return "\n".join(toc)

    def validateFormat(self, content: str, formatType: str) -> bool:
        """Validate content for a specific format."""
        if formatType == "json":
            try:
                json.loads(content)
                return True
            except json.JSONDecodeError:
                return False
        elif formatType == "markdown" or formatType == "html":
            return bool(content.strip())
        return False

    def convertFormat(self, content: str, fromFormat: str, toFormat: str) -> str:
        """Convert content between formats."""
        if fromFormat == "markdown" and toFormat == "html":
            return self.markdownToHtml(content)
        elif fromFormat == "markdown" and toFormat == "json":
            return self.markdownToJson(content)
        elif fromFormat == "json" and toFormat == "markdown":
            return self.jsonToMarkdown(content)
        elif fromFormat == "json" and toFormat == "html":
            return self.jsonToHtml(content)
        elif fromFormat == "html" and toFormat == "markdown":
            return self.htmlToMarkdown(content)
        elif fromFormat == toFormat:
            return content
        else:
            raise ValueError(f"Unsupported conversion: {fromFormat} -> {toFormat}")

    def batchConvert(self, content: str, fromFormat: str, toFormats: List[str]) -> Dict[str, str]:
        """Convert content to multiple formats at once."""
        results = {}
        for toFormat in toFormats:
            results[toFormat] = self.convertFormat(content, fromFormat, toFormat)
        return results

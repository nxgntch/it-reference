"""Format validation and optimization for documentation output."""

import json
import re
from typing import Any, Dict, List, Optional

from app.core.validation import ValidationResult


class FormatValidator:
    """Validate and optimize documentation formats."""

    def __init__(self):
        """Initialize format validator."""
        self.schema: Optional[Dict[str, Any]] = None
        self.strictMode = False

    def setSchema(self, schema: Dict[str, Any]) -> None:
        """Set JSON schema for validation."""
        self.schema = schema

    def validateJson(self, jsonStr: str) -> ValidationResult:
        """Validate JSON format and content."""
        errors = []
        warnings = []
        fixes = {}
        # Parse JSON
        try:
            data = json.loads(jsonStr)
        except json.JSONDecodeError as e:
            return ValidationResult(isValid=False, errors=[str(e)], warnings=[], fixes={})
        # Check schema if provided
        if self.schema:
            schemaErrors = self._validateJsonSchema(data, self.schema)
            errors.extend(schemaErrors)
        # Check for common issues
        if not isinstance(data, dict):
            errors.append("Root must be an object")
        if "title" in data and not isinstance(data["title"], str):
            errors.append("title must be a string")
        if "sections" in data and not isinstance(data["sections"], list):
            errors.append("sections must be an array")
        return ValidationResult(
            isValid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            fixes=fixes,
        )

    def validateMarkdown(self, markdown: str) -> ValidationResult:
        """Validate markdown format."""
        errors = []
        warnings = []
        fixes = {}
        if not markdown:
            return ValidationResult(isValid=True, errors=[], warnings=[], fixes={})
        lines = markdown.split("\n")
        # Check for common issues
        for i, line in enumerate(lines, 1):
            # Missing space after heading
            if re.match(r"^#+[^\s]", line):
                warnings.append(f"Line {i}: Missing space after heading markers")
            fixes[f"line_{i}"] = re.sub(r"^(#+)([^\s])", r"\1 \2", line)
            # Empty headings
            if re.match(r"^#+\s*$", line):
                errors.append(f"Line {i}: Empty heading")
            # Unbalanced backticks
            if line.count("`") % 2 != 0:
                warnings.append(f"Line {i}: Unbalanced backticks")
        return ValidationResult(
            isValid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            fixes=fixes,
        )

    def validateHtml(self, html: str) -> ValidationResult:
        """Validate HTML5 format."""
        errors = []
        warnings = []
        fixes = {}
        if not html:
            return ValidationResult(isValid=True, errors=[], warnings=[], fixes={})
        # Check for common issues
        if not html.lower().startswith("<!doctype"):
            warnings.append("Missing DOCTYPE declaration")
        # Unbalanced tags (exclude self-closing tags)
        selfClosing = {"img", "br", "hr", "input", "meta", "link"}
        openTags = re.findall(r"<(\w+)[^>]*(?<!/)>", html)
        closeTags = re.findall(r"</(\w+)>", html)
        openCount = {}
        closeCount = {}
        for tag in openTags:
            if tag.lower() not in selfClosing:
                openCount[tag] = openCount.get(tag, 0) + 1
        for tag in closeTags:
            closeCount[tag] = closeCount.get(tag, 0) + 1
        for tag in openCount:
            if openCount.get(tag, 0) != closeCount.get(tag, 0):
                errors.append(f"Unbalanced <{tag}> tags")
        # Check for deprecated tags
        deprecated = ["b", "i", "font", "center"]
        for tag in deprecated:
            if re.search(f"<{tag}[^>]*>", html, re.IGNORECASE):
                warnings.append(f"Deprecated tag <{tag}> found")
        # Missing alt text in images
        if "<img" in html:
            imgs = re.findall(r"<img[^>]*>", html)
            missingAlt = [img for img in imgs if "alt=" not in img]
            if missingAlt:
                warnings.append(f"{len(missingAlt)} images missing alt text")
        return ValidationResult(
            isValid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            fixes=fixes,
        )

    def normalizeMarkdown(self, markdown: str) -> str:
        """Normalize markdown format."""
        lines = markdown.split("\n")
        normalized = []
        for line in lines:
            # Fix missing space after heading
            line = re.sub(r"^(#+)([^\s#])", r"\1 \2", line)
            # Normalize multiple spaces
            line = re.sub(r"  +", " ", line)
            # Trim trailing whitespace
            line = line.rstrip()
            normalized.append(line)
        # Remove consecutive blank lines
        result = []
        prevBlank = False
        for line in normalized:
            if not line.strip():
                if not prevBlank:
                    result.append(line)
                prevBlank = True
            else:
                result.append(line)
                prevBlank = False
        return "\n".join(result)

    def optimizeJson(self, jsonStr: str, minify: bool = False) -> str:
        """Optimize JSON format."""
        try:
            data = json.loads(jsonStr)
        except json.JSONDecodeError:
            return jsonStr
        if minify:
            return json.dumps(data, separators=(",", ":"))
        else:
            return json.dumps(data, indent=2)

    def _validateJsonSchema(self, data: Any, schema: Dict[str, Any]) -> List[str]:
        """Validate data against JSON schema."""
        errors = []
        if "type" in schema:
            expected = schema["type"]
            actual = type(data).__name__
            if expected == "object" and not isinstance(data, dict):
                errors.append(f"Expected object, got {actual}")
            elif expected == "array" and not isinstance(data, list):
                errors.append(f"Expected array, got {actual}")
            elif expected == "string" and not isinstance(data, str):
                errors.append(f"Expected string, got {actual}")
        if "properties" in schema and isinstance(data, dict):
            for prop, propSchema in schema["properties"].items():
                if prop in data:
                    propErrors = self._validateJsonSchema(data[prop], propSchema)
                    errors.extend(propErrors)
        if "required" in schema and isinstance(data, dict):
            for required in schema["required"]:
                if required not in data:
                    errors.append(f"Missing required field: {required}")
        return errors

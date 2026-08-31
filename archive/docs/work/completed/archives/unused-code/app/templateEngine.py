"""Template engine for custom documentation generation with Jinja2-compatible syntax."""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class TemplateVariable:
    """Template variable definition."""

    name: str
    value: Any
    required: bool = False
    description: str = ""


class TemplateError(Exception):
    """Template processing error."""

    pass


class TemplateEngine:
    """Template engine for Jinja2-compatible markdown and HTML generation."""

    def __init__(self, templatesDir: Optional[str] = None):
        """Initialize template engine with optional templates directory."""
        self.templatesDir = Path(templatesDir) if templatesDir else None
        self.cache = {}
        self.variables: Dict[str, TemplateVariable] = {}
        self.filters: Dict[str, callable] = self._initializeFilters()

    def _initializeFilters(self) -> Dict[str, callable]:
        """Initialize built-in filters."""
        return {
            "upper": lambda x: str(x).upper(),
            "lower": lambda x: str(x).lower(),
            "title": lambda x: str(x).title(),
            "length": lambda x: len(x),
            "reverse": lambda x: "".join(reversed(str(x))),
            "trim": lambda x: str(x).strip(),
        }

    def registerVariable(
        self, name: str, value: Any, required: bool = False, description: str = ""
    ) -> None:
        """Register a template variable."""
        self.variables[name] = TemplateVariable(
            name=name, value=value, required=required, description=description
        )

    def registerFilter(self, name: str, fn: callable) -> None:
        """Register a custom filter function."""
        self.filters[name] = fn

    def loadTemplate(self, path: str) -> str:
        """Load template from file or cache."""
        if path in self.cache:
            return self.cache[path]
        if not self.templatesDir:
            raise TemplateError("Templates directory not configured")
        templatePath = self.templatesDir / path
        if not templatePath.exists():
            raise TemplateError(f"Template not found: {path}")
        with open(templatePath, "r", encoding="utf-8") as f:
            content = f.read()
        self.cache[path] = content
        return content

    def validateTemplate(self, template: str) -> bool:
        """Validate template syntax."""
        try:
            # Check for balanced braces and tags
            openBraces = template.count("{{") + template.count("{%")
            closeBraces = template.count("}}") + template.count("%}")
            if openBraces != closeBraces:
                return False
            # Check for unterminated tags
            return not re.search(r"\{\{(?!\s*\w)", template)
        except Exception:
            return False

    def renderMarkdown(self, template: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """Render markdown template with variables."""
        if not self.validateTemplate(template):
            raise TemplateError("Invalid template syntax")
        context = self._buildContext(variables)
        rendered = self._processTemplate(template, context)
        return rendered

    def renderHTML(self, template: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """Render HTML template with variables."""
        if not self.validateTemplate(template):
            raise TemplateError("Invalid template syntax")
        context = self._buildContext(variables)
        rendered = self._processTemplate(template, context)
        return rendered

    def _buildContext(self, variables: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Build rendering context from registered and provided variables."""
        context = {}
        # Add registered variables
        for name, var in self.variables.items():
            context[name] = var.value
        # Override with provided variables
        if variables:
            context.update(variables)
        # Verify required variables (only check if value is provided or empty string)
        for name, var in self.variables.items():
            if var.required and name in context and not context[name]:
                raise TemplateError(f"Required variable missing: {name}")
        return context

    def _processTemplate(self, template: str, context: Dict[str, Any]) -> str:
        """Process template with variable substitution and filters."""
        result = template
        # Process loops first (they add variables to context)
        result = self._processLoops(result, context)
        # Process conditionals next
        result = self._processConditionals(result, context)
        # Process variable substitution last
        varPattern = r"\{\{\s*(\w+)(?:\s*\|\s*(\w+))?\s*\}\}"
        result = re.sub(varPattern, lambda m: self._substituteVariable(m, context), result)
        return result

    def _substituteVariable(self, match: re.Match, context: Dict[str, Any]) -> str:
        """Substitute a variable with optional filter."""
        varName = match.group(1)
        filterName = match.group(2)
        if varName not in context:
            raise TemplateError(f"Undefined variable: {varName}")
        value = context[varName]
        if filterName:
            if filterName not in self.filters:
                raise TemplateError(f"Undefined filter: {filterName}")
            value = self.filters[filterName](value)
        return str(value)

    def _processConditionals(self, template: str, context: Dict[str, Any]) -> str:
        """Process if/else conditionals."""
        # Pattern: {% if variable %} ... {% else %} ... {% endif %}
        pattern = r"\{%\s*if\s+(\w+)\s*%\}(.*?)\{%\s*endif\s*%\}"
        elsePattern = r"(.*?)\{%\s*else\s*%\}(.*?)$"

        def processIf(match: re.Match) -> str:
            varName = match.group(1)
            content = match.group(2)
            if varName not in context:
                raise TemplateError(f"Undefined variable in conditional: {varName}")
            # Check for else block
            elseMatch = re.search(elsePattern, content, re.DOTALL)
            if elseMatch:
                ifContent = elseMatch.group(1)
                elseContent = elseMatch.group(2)
                return ifContent if context[varName] else elseContent
            else:
                return content if context[varName] else ""

        result = re.sub(pattern, processIf, template, flags=re.DOTALL)
        return result

    def _processLoops(self, template: str, context: Dict[str, Any]) -> str:
        """Process for loops."""
        # Pattern: {% for item in items %} ... {% endfor %}
        pattern = r"\{%\s*for\s+(\w+)\s+in\s+(\w+)\s*%\}(.*?)\{%\s*endfor\s*%\}"

        def processFor(match: re.Match) -> str:
            itemVar = match.group(1)
            listVar = match.group(2)
            loopContent = match.group(3)
            if listVar not in context:
                raise TemplateError(f"Undefined list in loop: {listVar}")
            items = context[listVar]
            if not isinstance(items, (list, tuple)):
                raise TemplateError(f"Loop variable must be iterable: {listVar}")
            result = []
            for _item in items:
                loopContext = context.copy()
                loopContext[itemVar] = _item
            rendered = self._processTemplate(loopContent, loopContext)
            result.append(rendered)
            return "".join(result)

        result = re.sub(pattern, processFor, template, flags=re.DOTALL)
        return result

    def renderFile(self, path: str, variables: Optional[Dict[str, Any]] = None) -> str:
        """Render template from file."""
        template = self.loadTemplate(path)
        fileFormat = path.split(".")[-1].lower()
        if fileFormat == "html":
            return self.renderHTML(template, variables)
        else:
            return self.renderMarkdown(template, variables)

    def batchRender(
        self, templates: Dict[str, str], variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """Render multiple templates with same variables."""
        results = {}
        for name, template in templates.items():
            results[name] = self.renderMarkdown(template, variables)
        return results

    def getVariableInfo(self) -> List[Dict[str, Any]]:
        """Get information about registered variables."""
        return [
            {
                "name": var.name,
                "required": var.required,
                "description": var.description,
                "value": str(var.value)[:100],  # Truncate for display
            }
            for var in self.variables.values()
        ]

    def getFilterInfo(self) -> List[str]:
        """Get list of available filters."""
        return list(self.filters.keys())

    def clearCache(self) -> None:
        """Clear template cache."""
        self.cache.clear()

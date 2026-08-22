# Changelog

All notable changes to NXGNTCH plugin are documented in this file.

## [2.0.0] — 2026-08-10

### Changed
- **Repository Cleanup**: Moved development utilities (nxgntch/) to tools/ directory
- **Documentation**: Removed redundant/outdated files (MODULE_INVENTORY.md, MANIFEST.md, INDEX.md)
- **Documentation**: Renamed agents.md to AGENT_ARCHITECTURE.md for clarity
- **Configuration**: Removed duplicate .claude/settings.json (single source of truth)
- **Version**: Synchronized version across all config files (pyproject.toml, README.md, plugin manifests)

### Fixed
- Agent naming consistency (corrected snakeCase references to camelCase in documentation)
- AUDIT.md agent inventory (organized by tier: Opus 5, Sonnet 5, Haiku 4.5)
- Documentation links and version numbers across all files

### Documentation
- Updated docs/README.md as single source of truth for documentation index
- Verified all agent descriptions and skill references
- Updated changelog and audit documentation

---

## [1.1.0] — 2026-08-10

### Added
- Marketplace plugin restructuring to match nxgntch/it engineering patterns
- AUDIT.md with plugin health metrics and phase roadmap
- Engineering standards via CLAUDE.md and .claude/rules/
- Configuration framework (agents.yaml, models.yaml, skills.yaml, governance.yaml, orchestration.yaml)
- Development tooling (pyproject.toml, pytest configuration)

### Changed
- Updated README.md with improved structure and documentation links
- Merged engineering standards from nxgntch/it while preserving plugin functionality

### Fixed
- Aligned agent and skill naming conventions (snakeCase enforcement)

---

## [1.0.0] — Initial Release

First stable release of NXGNTCH marketplace plugin.

---

**See [releases](https://github.com/nxgntch/NXGNTCH/releases) for full history.**

# Archived & Legacy Documentation

Historical content, deprecated files, and legacy references.

---

## Why This Exists

This map preserves links to archived and deprecated documentation for historical context. Most users should reference current documentation in other sectioned maps.

---

## Deprecated Documentation

**No longer actively maintained. Reference for historical context only:**

- **[docs/archive/](archive/)** — Archived documentation directory
- **[docs/phases/](phases/)** — Historical phase documentation
  - **[docs/phases/PHASE_9.md](phases/PHASE_9.md)** — Phase 9 documentation (Quality Hardening)
  - **[docs/archive/phases/phase7.md](archive/phases/phase7.md)** — Phase 7 archived

---

## Legacy References

**Old naming conventions and documentation (superseded):**

- **[docs/AGENTS_REFERENCE.md](AGENTS_REFERENCE.md)** — Legacy agent reference (see AGENTS_FULL_REFERENCE.md instead)
- **[docs/AGENTS_REFERENCE_AUTO.md](AGENTS_REFERENCE_AUTO.md)** — Auto-generated legacy reference
- **[docs/SKILLS_REFERENCE_AUTO.md](SKILLS_REFERENCE_AUTO.md)** — Auto-generated legacy skills reference
- **[docs/SKILL_INVENTORY.md](SKILL_INVENTORY.md)** — Legacy skills inventory (see SKILLS_REFERENCE.md)
- **[docs/SYNC_CONFIG_GUIDE.md](SYNC_CONFIG_GUIDE.md)** — Legacy sync configuration guide
- **[docs/TROUBLESHOOTING.md](TROUBLESHOOTING.md)** — Legacy troubleshooting

---

## Deprecated Link Map

**Original monolithic link map (superseded by sectioned maps):**

- **[docs/LINK_MAP.md](LINK_MAP.md)** — Deprecated: Use sectioned maps instead
  - Total size: 345 KB, 7,347 lines
  - Replaced by: [LINKS_NAVIGATION.md](LINKS_NAVIGATION.md), [LINKS_CORE_DOCS.md](LINKS_CORE_DOCS.md), [LINKS_REFERENCE.md](LINKS_REFERENCE.md), [LINKS_SKILLS_AGENTS.md](LINKS_SKILLS_AGENTS.md), [LINKS_ARCHIVE.md](LINKS_ARCHIVE.md)
  - Combined size: < 50 KB (88% reduction)

---

## Legacy Project Files

**Older project files not in active use:**

- **[CHANGELOG.md](../CHANGELOG.md)** — Historical changelog (superseded by git log)
- **[GETTING_STARTED.md](../GETTING_STARTED.md)** — Legacy getting started guide (see README.md instead)

---

## Archive Directory Structure

**Location of archived documentation:**

```
docs/
├── archive/                    # Archived & legacy docs
│   ├── phases/
│   │   ├── phase7.md
│   │   └── ...
│   └── ...
└── phases/                     # Historical phase docs
    ├── PHASE_9.md
    └── ...
```

---

## When to Use Archive

Use archived documentation when:
- Looking for **historical context** on how the system evolved
- Investigating **old decisions** or why something changed
- Researching **legacy code paths** (may still be in production)
- Understanding **deprecated patterns** (to avoid repeating them)

**Don't use** for current development — reference current sectioned maps instead.

---

## Migration Path

If you find yourself in archived docs:

| Old Doc | New Location |
|---------|--------------|
| AGENTS_REFERENCE.md | [AGENTS_FULL_REFERENCE.md](AGENTS_FULL_REFERENCE.md) |
| SKILLS_REFERENCE.md | [SKILLS_REFERENCE.md](SKILLS_REFERENCE.md) |
| LINK_MAP.md | Sectioned maps (see [LINKS_NAVIGATION.md](LINKS_NAVIGATION.md)) |
| Phase X docs | [AUDIT.md](../AUDIT.md) (living status) |
| GETTING_STARTED.md | [README.md](../README.md) |
| TROUBLESHOOTING.md | [AUDIT.md](../AUDIT.md) or specific rule file |

---

## See Also

- **Current navigation** — [LINKS_NAVIGATION.md](LINKS_NAVIGATION.md)
- **Core documentation** — [LINKS_CORE_DOCS.md](LINKS_CORE_DOCS.md)
- **Development standards** — [LINKS_REFERENCE.md](LINKS_REFERENCE.md)
- **Skills & agents** — [LINKS_SKILLS_AGENTS.md](LINKS_SKILLS_AGENTS.md)

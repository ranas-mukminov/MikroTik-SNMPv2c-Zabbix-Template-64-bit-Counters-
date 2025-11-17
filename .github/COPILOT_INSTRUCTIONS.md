# GitHub Copilot Instructions for MikroTik-SNMPv2c-Zabbix-Template

## Overview

This document contains instructions for GitHub Copilot and other AI coding assistants when working with the `ranas-mukminov/MikroTik-SNMPv2c-Zabbix-Template-64-bit-Counters-` repository.

**Repository Owner:** Ranas Mukminov  
**Repository:** https://github.com/ranas-mukminov/MikroTik-SNMPv2c-Zabbix-Template-64-bit-Counters-  
**Default Branch:** `main`

---

## Important Constraints

### What You Must NOT Do

AI assistants must **NEVER**:

- Create PRs or push directly to the repository
- Run git commands yourself (except for local inspection)
- Rename or remove existing template files:
  - `template_mikrotik_snmpv2c_advanced_zbx72.xml`
  - `template_mikrotik_snmpv3_advanced_zbx72.xml`
  - `template_mikrotik_snmpv2c_zbx72_uuid32.xml`
- Change Zabbix template names, keys, or item prototypes in a breaking way
- Change monitored metric names or SNMP OIDs
- Downgrade supported versions (Zabbix 7.0+, RouterOS 6.x/7.x)
- Inject marketing, pricing, or commercial offers
- Use `git push --force` or `git reset --hard`

### What You Should Do

Your role is to:

1. **Generate exact file contents** (final state, not diffs)
2. **Propose safe git workflow** (commands for the owner to run)
3. **Generate PR title + body** (for GitHub UI)

All branches and PRs are in the `origin` remote: `ranas-mukminov/MikroTik-SNMPv2c-Zabbix-Template-64-bit-Counters-`

---

## Repository Context

### Project Summary

- **Purpose:** Production-ready Zabbix templates for MikroTik RouterOS monitoring
- **Focus:**
  - MikroTik monitoring via SNMPv2c and SNMPv3
  - 64-bit counters for high-speed links (10G+)
  - Enterprise-style triggers, macros, and discovery

### Main Template Files

| File | Description |
|------|-------------|
| `template_mikrotik_snmpv2c_advanced_zbx72.xml` | Advanced SNMPv2c template with 64-bit counters |
| `template_mikrotik_snmpv3_advanced_zbx72.xml` | Advanced SNMPv3 template with auth+priv |
| `template_mikrotik_snmpv2c_zbx72_uuid32.xml` | Legacy/basic SNMPv2c template |

### Documentation Structure

| File/Directory | Purpose |
|----------------|---------|
| `README.md` | Main English documentation |
| `CHANGELOG.md` | Version history (v2.0, etc.) |
| `examples/` | Example host/template usage |
| `tests/` | Automated checks |
| `.github/workflows` | CI validation workflows |

### Compatibility Requirements

- **Zabbix:** 7.0+
- **RouterOS:** 6.x/7.x

---

## Typical Tasks

When asked to:

- "обнови README и подготовь PR" (update README and prepare PR)
- "добавь README.ru.md и оформи PR" (add Russian README and create PR)
- "расширь раздел Monitored Metrics" (expand Monitored Metrics section)
- "обнови примеры по SNMPv3" (update SNMPv3 examples)

You must:

1. **Preserve technical model:**
   - Templates remain unchanged unless explicitly requested
   - Macro names must stay consistent with README and XML
   - SNMPv2c/SNMPv3 examples must be valid for MikroTik RouterOS

2. **Prefer documentation changes first:**
   - Update `README.md` (English)
   - Create/update `README.ru.md` (Russian), if requested
   - Update `examples/` content
   - Update `CHANGELOG.md` if version bump requested

3. **Only change XML templates when explicitly asked:**
   - Keep Zabbix 7.0+ import compatibility
   - Keep tags, macros, items, triggers consistent with documentation

---

## Required Output Structure

Every response must follow this **5-section structure**:

### 1. Summary of Changes

Short bullet list in English:

```
- `README.md`: clarified SNMPv3 setup and macros usage
- `README.ru.md`: added Russian documentation
- `CHANGELOG.md`: documented v2.1 docs update
```

### 2. Files to Change/Create

List all files touched:

```
README.md                             – updated English documentation
README.ru.md                          – new Russian documentation
CHANGELOG.md                          – updated changelog entry
examples/mikrotik_snmpv3_host.md      – new SNMPv3 example
```

### 3. Final File Contents

Show **complete final content** for each file (not diffs):

```markdown
<!-- README.md -->
```markdown
# MikroTik SNMP Zabbix Templates (Production-Ready v2.1)
...
[full file content]
```

Rules:
- Output **entire** file content (no truncation)
- Keep Markdown formatting valid
- Use English in `README.md`, Russian in `README.ru.md`
- Respect existing CHANGELOG style (newest first)

### 4. Git Commands

Provide ready-to-run commands:

```bash
# 1. Update local main
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b docs/update-mikrotik-snmp-readme

# 3. Apply changes (edit files as shown above)

# 4. Review changes
git status
git diff

# 5. Commit
git add README.md README.ru.md CHANGELOG.md
git commit -m "docs: improve MikroTik SNMP Zabbix template documentation"

# 6. Push to origin
git push -u origin docs/update-mikrotik-snmp-readme
```

Branch naming conventions:
- `docs/<short-topic>` - documentation changes
- `feat/<short-topic>` - new features
- `fix/<short-topic>` - bug fixes

Examples:
- `docs/add-russian-readme`
- `docs/improve-snmpv3-examples`
- `feat/add-new-mikrotik-macros-docs`

### 5. PR Title and Body

Generate PR content for GitHub UI:

```
PR title:
docs: improve MikroTik SNMP Zabbix template documentation

PR body (Markdown):

## Summary

- Updated README.md with clearer SNMPv2c/SNMPv3 setup steps
- Added README.ru.md as Russian translation
- Extended macro reference and security best practices sections

## Changes

- README.md
- README.ru.md
- CHANGELOG.md

## Motivation

This PR improves documentation for MikroTik SNMP Zabbix templates, making it easier for network engineers to deploy templates securely.

## Checklist

- [x] README renders correctly on GitHub
- [x] Examples stay consistent with existing templates
- [x] No breaking changes to template XML, keys, or triggers
```

Language:
- PR title in **English** by default
- PR body in **English** by default (or Russian if explicitly requested)

---

## Documentation Style Guidelines

### For README.md (English)

Keep existing structure:
- Overview
- Available Templates
- Features
- Quick Start
- Security Best Practices
- Detailed Configuration (macros reference)
- Monitored Metrics
- Triggers and Alerting
- Customization
- Troubleshooting
- Examples
- Professional Support / Contact
- Changelog link

When updating:
- Do not contradict SNMP configuration examples
- Keep macro names exact: `{$SNMP_COMMUNITY}`, `{$IF.*}`, `{$CPU.*}`, etc.
- Emphasize 64-bit counters and Zabbix 7.0+ compatibility

### For README.ru.md (Russian)

- Natural Russian text (not literal translation)
- Mirror README.md structure (Обзор, Доступные шаблоны, etc.)
- Keep metric names, filenames, macros, OIDs in English
- Use proper Russian terminology for networking/monitoring

### For Examples

- Minimal, realistic examples
- Zabbix host configuration notes
- MikroTik CLI snippets
- Generic names: `mikrotik-router-01`, `DataCenter-1`, `10.0.0.100/32`

### For CHANGELOG.md

- Follow existing format
- Add new version entry at top for significant changes
- Use semantic versioning

---

## Command & Configuration Style

### MikroTik RouterOS Syntax

```bash
/snmp
set enabled=yes

/snmp community
set [find default=yes] name="MySecureString123!" addresses=10.0.0.100/32
```

### Zabbix UI Steps

Use ordered lists:

```
1. Go to Configuration → Templates
2. Click Import
3. Select file...
```

### Macros

Always show with braces:

```
{$SNMP_COMMUNITY}
{$SNMPV3_USER}
{$CPU.UTIL.WARN}
```

---

## Output Contract

Always:

1. Follow the 5-section structure (summary, files, contents, git commands, PR)
2. Do not add meta explanations like "Here is..." or "As an AI..."
3. Do not mention that you cannot run commands
4. Just generate clear, actionable instructions

---

## Examples of Proper Responses

### Example 1: Update README with SNMPv3 clarifications

**What user asks:**
> "Улучши раздел Security Best Practices в README и подготовь PR"

**Your response structure:**

```
### 1. Summary of changes

- `README.md`: expanded Security Best Practices section with SNMPv3 configuration examples
- `CHANGELOG.md`: added v2.1 documentation update entry

### 2. Files to change / create

README.md      – updated Security Best Practices section
CHANGELOG.md   – added version entry

### 3. Final file contents

<!-- README.md -->
[complete file content here]

<!-- CHANGELOG.md -->
[complete file content here]

### 4. Git commands

git checkout main
git pull origin main
git checkout -b docs/improve-security-best-practices
[... rest of commands]

### 5. PR title and body

PR title:
docs: expand Security Best Practices section with SNMPv3 examples

PR body:
[... proper formatted body]
```

---

## Version History

- **2025-11-17:** Initial creation of Copilot instructions
- Template structure and guidelines documented
- Output format requirements defined

---

## Questions?

If instructions are unclear or you need to do something not covered here, ask the repository owner before proceeding.

**Never** guess about breaking changes or template modifications.

# AI Assistant Collaboration Guide

## For Repository Maintainers

This guide explains how to effectively work with GitHub Copilot and other AI coding assistants on this repository.

---

## Quick Start

### Typical Request Format

When you want to update documentation or make changes:

**Russian (natural):**
```
"Обнови README, расширь раздел Security Best Practices и подготовь PR"
"Добавь README.ru.md с русской документацией и оформи PR"
"Улучши примеры SNMPv3 конфигурации"
```

**English:**
```
"Update README, expand Security Best Practices section and prepare PR"
"Add README.ru.md with Russian documentation and create PR"
"Improve SNMPv3 configuration examples"
```

### What You Get Back

AI assistant will provide:

1. ✅ **Summary** - what changed
2. ✅ **File list** - all files modified
3. ✅ **Complete file contents** - ready to copy/paste
4. ✅ **Git commands** - ready to run in terminal
5. ✅ **PR template** - title and body for GitHub

---

## AI Assistant Capabilities

### ✅ What AI Can Do

- Generate/update documentation (README, examples, guides)
- Create Russian translations (README.ru.md)
- Update CHANGELOG with new versions
- Provide configuration examples (MikroTik, Zabbix)
- Suggest improvements to existing docs
- Create new example files
- Format markdown properly
- Ensure consistency across docs

### ❌ What AI Cannot Do

- Push code directly to repository
- Create PRs automatically
- Rename/delete template XML files
- Make breaking changes to templates
- Change SNMP OIDs or metric definitions
- Run git commands on your behalf

**You must:** Run git commands and create PRs manually

---

## Workflow Example

### Scenario: Add Russian README

**1. Your request:**
```
"Создай README.ru.md - русскую версию документации, и подготовь PR"
```

**2. AI response includes:**

```markdown
### 1. Summary of changes
- `README.ru.md`: created Russian version of main documentation
- `CHANGELOG.md`: added v2.1 entry for Russian docs
- `README.md`: added link to Russian version

### 2. Files to change/create
README.md       – added language switcher
README.ru.md    – new Russian documentation
CHANGELOG.md    – version update

### 3. Final file contents
[Complete content for each file]

### 4. Git commands
git checkout main
git pull origin main
git checkout -b docs/add-russian-readme
# [edit files as shown above]
git add README.md README.ru.md CHANGELOG.md
git commit -m "docs: add Russian README translation"
git push -u origin docs/add-russian-readme

### 5. PR title and body
[Ready-to-paste PR description]
```

**3. You execute:**

Copy the file contents, run the git commands, create PR on GitHub.

---

## Common Tasks

### Task 1: Update Existing Documentation

**Request:**
```
"Улучши раздел 'Monitored Metrics' в README - добавь больше деталей про OSPF и BGP метрики"
```

**AI provides:**
- Updated README.md (full content)
- Updated CHANGELOG.md
- Git commands
- PR template

**You do:**
1. Copy new README.md content
2. Copy new CHANGELOG.md content
3. Run provided git commands
4. Create PR with provided title/body

### Task 2: Add New Examples

**Request:**
```
"Создай новый пример конфигурации для SNMPv3 с AES256 шифрованием"
```

**AI provides:**
- New file: `examples/mikrotik_snmpv3_aes256.md`
- Updated `README.md` (link to new example)
- Updated `CHANGELOG.md`
- Git commands
- PR template

### Task 3: Fix Documentation Issue

**Request:**
```
"В разделе Quick Start ошибка - неправильная команда MikroTik. Исправь"
```

**AI provides:**
- Fixed README.md
- Explanation of what was wrong
- Git commands
- PR template

---

## Best Practices

### ✅ Do

- **Be specific:** "Expand Security Best Practices section with firewall examples"
- **Specify language:** "Create Russian version" or "в русской локализации"
- **Reference sections:** "Update the Troubleshooting section"
- **Request review:** "Show me the diff before committing"

### ❌ Don't

- **Be vague:** "Make docs better"
- **Request breaking changes:** "Rename all template files"
- **Skip verification:** Always review generated content
- **Forget versioning:** Update CHANGELOG for significant changes

---

## Safety Checklist

Before pushing AI-generated changes:

- [ ] Review all file contents for accuracy
- [ ] Check that examples match actual template capabilities
- [ ] Verify macro names match template XML
- [ ] Test markdown rendering (GitHub preview)
- [ ] Ensure no breaking changes to templates
- [ ] Verify SNMP OIDs are correct
- [ ] Check that version numbers are appropriate
- [ ] Confirm all links work

---

## File Structure Reference

### Core Files (Do Not Delete)

```
template_mikrotik_snmpv2c_advanced_zbx72.xml  ← Main SNMPv2c template
template_mikrotik_snmpv3_advanced_zbx72.xml   ← Main SNMPv3 template
template_mikrotik_snmpv2c_zbx72_uuid32.xml    ← Legacy template
README.md                                      ← Main documentation
CHANGELOG.md                                   ← Version history
```

### Documentation Files (Safe to Modify)

```
README.md                          ← Main English docs
README.ru.md                       ← Russian docs (if exists)
CHANGELOG.md                       ← Version history
examples/mikrotik_snmp_config.rsc  ← MikroTik config example
examples/zabbix_host_config_example.md  ← Zabbix setup guide
```

### Generated/Build Files (Ignore)

```
node_modules/     ← Dependencies
.github/          ← CI/CD configs
tests/            ← Test scripts
```

---

## Macro Reference (For AI Consistency)

When AI generates documentation, these macros must remain consistent:

### SNMP Authentication
- `{$SNMP_COMMUNITY}` - SNMPv2c community string
- `{$SNMPV3_USER}` - SNMPv3 username
- `{$SNMPV3_AUTH_PASSPHRASE}` - Auth password
- `{$SNMPV3_PRIV_PASSPHRASE}` - Privacy password

### Thresholds
- `{$CPU.UTIL.WARN}` / `{$CPU.UTIL.CRIT}` - CPU thresholds
- `{$MEM.UTIL.WARN}` / `{$MEM.UTIL.CRIT}` - Memory thresholds
- `{$TEMP.MAX.WARN}` / `{$TEMP.MAX.CRIT}` - Temperature
- `{$VOLTAGE.MIN}` / `{$VOLTAGE.MAX}` - Voltage

### Interface Discovery
- `{$IF.LLD.FILTER.MATCH}` - Include interfaces
- `{$IF.LLD.FILTER.NOT_MATCHES}` - Exclude interfaces
- `{$IF.LLD.FILTER.ADMIN_STATUS}` - Admin status filter
- `{$IF.POLL.INTERVAL}` - Polling frequency
- `{$IF.ERRORS.MAX_DELTA}` - Error threshold
- `{$IF.DISCARDS.MAX_DELTA}` - Discard threshold
- `{$IF.BROADCAST.MAX_PPS}` - Broadcast storm threshold

---

## Version Numbering

When updating CHANGELOG:

- **v2.0.x** - Documentation updates, minor fixes
- **v2.1.0** - New features, new templates, major docs
- **v3.0.0** - Breaking changes

Example CHANGELOG entry:

```markdown
## [2.1.0] - 2025-11-20

### Added
- Russian documentation (README.ru.md)
- New SNMPv3 AES256 example

### Changed
- Expanded Security Best Practices section

### Fixed
- Corrected MikroTik CLI syntax in Quick Start
```

---

## Language Guidelines

### English (README.md)

- Technical, professional tone
- Use standard networking terminology
- "MikroTik RouterOS", "Zabbix Server", "SNMP community"

### Russian (README.ru.md)

- Natural Russian, not literal translation
- Use accepted Russian IT terms
- Keep technical terms in English where appropriate:
  - "SNMP community" (not translated)
  - "MikroTik RouterOS" (not translated)
  - Macro names in English: `{$SNMP_COMMUNITY}`

---

## Troubleshooting AI Responses

### Issue: AI suggests breaking changes

**Problem:** AI wants to rename template files or change OIDs

**Solution:**
```
"Нет, не меняй имена шаблонов. Только обнови документацию."
"No, don't change template names. Only update documentation."
```

### Issue: AI output too verbose

**Problem:** AI provides excessive explanations

**Solution:**
```
"Дай только финальное содержимое файлов и git команды"
"Provide only final file contents and git commands"
```

### Issue: AI forgets macro names

**Problem:** Macro names don't match templates

**Solution:**
```
"Используй точные имена макросов из template_mikrotik_snmpv2c_advanced_zbx72.xml"
"Use exact macro names from template_mikrotik_snmpv2c_advanced_zbx72.xml"
```

---

## Contact & Support

- **Repository:** https://github.com/ranas-mukminov/MikroTik-SNMPv2c-Zabbix-Template-64-bit-Counters-
- **Issues:** GitHub Issues
- **Professional Support:** [run-as-daemon.ru](https://run-as-daemon.ru)

---

## Version History

- **2025-11-17:** Initial guide creation
- Workflow patterns documented
- Safety checklist defined

---

**Remember:** AI is a tool to help you work faster, but you are the final authority on all changes. Always review before committing!

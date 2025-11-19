# 🤝 Contributing Guidelines

Thank you for your interest in contributing to the MikroTik SNMP Zabbix Templates project! This document provides guidelines for contributing to this repository.

---

## 📋 Table of Contents

- [How to Contribute](#how-to-contribute)
- [Code Style](#code-style)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Community Guidelines](#community-guidelines)
- [Professional Support](#professional-support)

---

## 🚀 How to Contribute

### Ways to Contribute

1. **Report Bugs**
   - Use GitHub Issues to report bugs
   - Include template version, Zabbix version, and RouterOS version
   - Provide steps to reproduce the issue
   - Include relevant logs and screenshots

2. **Suggest Enhancements**
   - Open an issue to discuss new features or improvements
   - Explain the use case and expected benefits
   - Consider backwards compatibility

3. **Submit Code Changes**
   - Fix bugs or implement approved features
   - Follow the contribution workflow below
   - Ensure your changes don't break existing functionality

4. **Improve Documentation**
   - Fix typos and clarify instructions
   - Add examples and use cases
   - Translate documentation to other languages

### Contribution Workflow

1. **Fork the Repository**
   ```bash
   # Fork via GitHub UI, then clone your fork
   git clone https://github.com/YOUR-USERNAME/MikroTik-SNMPv2c-Zabbix-Template-64-bit-Counters-.git
   cd MikroTik-SNMPv2c-Zabbix-Template-64-bit-Counters-
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-number-description
   ```

3. **Make Your Changes**
   - Keep changes focused and atomic
   - Test thoroughly on real MikroTik devices
   - Update documentation if needed

4. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "type: concise description"
   ```
   
   Commit types:
   - `feat:` New features
   - `fix:` Bug fixes
   - `docs:` Documentation changes
   - `refactor:` Code refactoring
   - `test:` Adding or updating tests
   - `chore:` Maintenance tasks

5. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in the PR template completely

---

## 📝 Code Style

### XML Template Guidelines

1. **Naming Conventions**
   - Use clear, descriptive names for items, triggers, and discoveries
   - Follow existing naming patterns in the templates
   - Use consistent prefixes (e.g., `ifHC*` for 64-bit counters)

2. **Item Keys**
   - **DO NOT** change existing item keys without strong justification
   - Changing keys breaks existing deployments and dashboards
   - If changes are necessary, document migration steps

3. **Macros**
   - Use macros for configurable thresholds and filters
   - Document macro purpose and default values
   - Use descriptive macro names (e.g., `{$IF_UTIL_WARN}`)

4. **XML Formatting**
   - Use proper indentation (4 spaces)
   - Validate XML syntax before committing
   - Keep templates readable and well-organized

5. **Comments**
   - Add comments for complex calculations or non-obvious logic
   - Document why certain OIDs or approaches are used
   - Include references to MIB documentation when relevant

### Documentation Style

1. **Markdown Formatting**
   - Use headers appropriately (H1 for title, H2 for main sections, etc.)
   - Include code blocks with syntax highlighting
   - Use tables for structured data
   - Add emojis for visual hierarchy

2. **Language**
   - Write in clear, concise English
   - Use technical terms correctly
   - Provide Russian translations for major documentation

3. **Examples**
   - Include practical, tested examples
   - Use realistic values and scenarios
   - Explain what the example demonstrates

---

## 🧪 Testing Requirements

### Before Submitting a PR

1. **XML Validation**
   ```bash
   # Validate XML syntax
   xmllint --noout template_mikrotik_snmpv2c_advanced_zbx72.xml
   ```

2. **Template Import Test**
   - Import the template into a test Zabbix instance
   - Verify no errors during import
   - Check that all items, triggers, and discoveries are created

3. **Functional Testing**
   - Link the template to a real MikroTik device
   - Verify data collection works correctly
   - Test discovery rules (interfaces, OSPF neighbors, etc.)
   - Verify triggers activate under expected conditions

4. **Version Compatibility**
   - Test with the minimum supported Zabbix version (7.2+)
   - Test with the latest Zabbix version if possible
   - Test with both RouterOS 6.x and 7.x

5. **Documentation Updates**
   - Update README if functionality changes
   - Update CHANGELOG.md with your changes
   - Add or update examples if relevant

### What to Test

- ✅ SNMP connectivity and data collection
- ✅ Interface discovery and filtering
- ✅ Trigger behavior (activation and recovery)
- ✅ Macro customization
- ✅ Graph and dashboard display
- ✅ Performance (polling interval, server load)

### Test Environment

Provide in your PR:
- Zabbix version used for testing
- RouterOS version and device model
- Any specific configuration required
- Screenshots of working features

---

## 🔄 Pull Request Process

### PR Title and Description

**Title Format:**
```
type: Short description (max 72 characters)
```

**Description Must Include:**
- Summary of changes
- Motivation and context
- Testing performed
- Breaking changes (if any)
- Related issues (fixes #123)

### PR Checklist

Before submitting, ensure:

- [ ] XML templates are valid and import successfully
- [ ] Changes tested on real MikroTik device
- [ ] Documentation updated (README, CHANGELOG)
- [ ] No hardcoded credentials or sensitive data
- [ ] Existing item keys not changed (unless justified)
- [ ] Backwards compatibility maintained (or migration path provided)
- [ ] Commit messages follow conventions
- [ ] PR description complete

### Review Process

1. **Automated Checks**
   - XML validation (if CI/CD configured)
   - Documentation syntax check

2. **Manual Review**
   - Maintainer reviews code and functionality
   - May request changes or additional testing
   - Discussion of implementation approach

3. **Approval and Merge**
   - PR approved by maintainer
   - Merged into main branch
   - Included in next release

### After Your PR is Merged

- Your contribution will be credited in CHANGELOG.md
- Major contributions may be highlighted in release notes
- You'll be listed as a contributor on GitHub

---

## 🌟 Community Guidelines

### Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

### Communication

- Be respectful and professional
- Stay on topic in discussions
- Help others when you can
- Accept constructive feedback gracefully

### Best Practices

1. **Before Starting Work**
   - Check existing issues and PRs
   - Discuss major changes in an issue first
   - Avoid duplicate work

2. **While Working**
   - Keep your fork updated
   - Make focused, incremental commits
   - Write clear commit messages

3. **Getting Help**
   - Ask questions in issues or discussions
   - Provide context and details
   - Be patient waiting for responses

---

## 🏢 Professional Support

Need help with contributions or custom development?

### Development Services

- 🛠️ **Custom Template Development**
  - Tailored monitoring templates for specific use cases
  - Integration with custom MikroTik configurations
  - Advanced metric collection and processing

- 🔧 **Template Optimization**
  - Performance tuning for large deployments
  - Custom discovery rules and filtering
  - Advanced trigger logic and alerting

- 📚 **Documentation and Training**
  - Internal documentation for your templates
  - Team training on template development
  - Best practices workshops

- 🤖 **Automation and Integration**
  - Monitoring-as-code implementation
  - CI/CD for template deployment
  - Integration with other monitoring tools

### Contact for Professional Development Support

> **"Defense by design. Speed by default."**

- 🌐 Website: [run-as-daemon.ru](https://run-as-daemon.ru)
- 💬 Telegram: [@run_as_daemon](https://t.me/run_as_daemon)
- 📱 VK: Available via website
- 💼 WhatsApp: Available via website
- 🐙 GitHub: [@ranas-mukminov](https://github.com/ranas-mukminov)

---

## 🙏 Thank You!

Thank you for contributing to the MikroTik SNMP Zabbix Templates project. Your contributions help make network monitoring better for everyone!

**Maintainer:** Ranas Mukminov | [run-as-daemon.ru](https://run-as-daemon.ru)

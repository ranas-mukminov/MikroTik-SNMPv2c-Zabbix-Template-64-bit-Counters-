# Contributing guide

Thank you for considering a contribution to the Homelab / SMB IaC blueprints and cost optimizer project! We welcome pull requests that improve documentation, add blueprints, extend collectors/estimators, or enhance AI integrations.

## How to contribute

1. **Discuss first** – Open an issue describing the problem or proposal. For new blueprints include diagrams, assumptions, and required variables.
2. **Create a branch** – Follow `feature/<short-description>` naming.
3. **Keep scope focused** – Separate PRs for docs, IaC, or Python changes when possible.
4. **Follow style** – Use `.editorconfig`, run `scripts/format.sh`, and ensure Terraform/Ansible lint passes.
5. **Add tests** – New Python code must include unit tests; blueprints should have validation notes or automated tests.
6. **Document** – Update `README.md`, blueprint READMEs, or `docs/` as needed so users understand your change.

## Development environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e optimizer/[tests]
pip install -r requirements.txt  # optional legacy dependencies
```

Run the quality gates:

```bash
scripts/lint.sh
scripts/security_scan.sh
pytest
```

## Blueprint submissions

* Include diagrams or textual topology descriptions in `blueprints/docs/`.
* Provide Terraform variable tables and Ansible inventory examples.
* Do not hardcode credentials. Use variables or vault integrations.
* Mention provider/API limitations and licensing requirements.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Be respectful and collaborative.

## Professional contact

For commercial support, training, or custom automation please visit [run-as-daemon.ru](https://run-as-daemon.ru).

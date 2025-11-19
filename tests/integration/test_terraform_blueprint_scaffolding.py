import shutil
import subprocess
from pathlib import Path

import pytest

BLUEPRINT_ROOT = Path("blueprints/terraform")


def terraform_available() -> bool:
    return shutil.which("terraform") is not None


@pytest.mark.parametrize("blueprint", ["proxmox-homelab", "k3s-ci-monitoring", "micro-saas"])
def test_blueprint_has_required_files(blueprint: str):
    path = BLUEPRINT_ROOT / blueprint
    assert (path / "main.tf").exists()
    assert (path / "variables.tf").exists()
    assert (path / "outputs.tf").exists()


@pytest.mark.skipif(not terraform_available(), reason="Terraform binary not available in test environment")
def test_terraform_validate(tmp_path: Path):
    blueprint = BLUEPRINT_ROOT / "proxmox-homelab"
    tmp_dir = tmp_path / "tf"
    shutil.copytree(blueprint, tmp_dir, dirs_exist_ok=True)
    subprocess.run(["terraform", "init"], cwd=tmp_dir, check=True)
    subprocess.run(["terraform", "validate"], cwd=tmp_dir, check=True)

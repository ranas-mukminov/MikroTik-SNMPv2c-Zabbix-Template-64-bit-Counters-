# Proxmox homelab blueprint

This Terraform blueprint provisions a Proxmox-based homelab consisting of:

* pfSense or OpenWrt firewall VM connected to WAN and LAN VLANs
* NAS VM with configurable disk size
* K3s worker nodes backed by a simple module (`modules/k3s-node`)

## Prerequisites

* Terraform 1.4+
* A Proxmox API token with sufficient privileges
* Remote state backend (configure via `terraform init -backend-config=...`)

## Usage

1. Copy `terraform.tfvars.example` (create one based on `variables.tf`).
2. Run `terraform init` in a dedicated workspace, e.g., `terraform workspace new homelab`.
3. Apply with `terraform apply`.

## Notes

* This blueprint does not create storage pools; reference existing pools via the `nodes.storage_pool` attribute.
* Add more modules for NAS replicas or Ceph integration as needed.
* Integrate with `blueprints/ansible` playbooks after provisioning.

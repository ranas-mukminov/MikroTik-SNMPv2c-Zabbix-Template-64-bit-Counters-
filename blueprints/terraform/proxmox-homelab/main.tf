locals {
  management_nodes = [for node in var.nodes : node if node.management]
  compute_nodes    = [for node in var.nodes : node if node.management == false]
}

provider "proxmox" {
  pm_api_url          = var.proxmox_api_url
  pm_api_token_id     = var.proxmox_token_id
  pm_api_token_secret = var.proxmox_token_secret
}

# Example blueprint for a pfSense firewall VM
resource "proxmox_vm_qemu" "pfsense" {
  name        = "edge-fw"
  target_node = local.management_nodes[0].name
  clone       = "pfsense-golden"
  cores       = 2
  sockets     = 1
  memory      = 4096
  scsihw      = "virtio-scsi-single"

  network {
    bridge = "vmbr0"
    tag    = var.vlans["wan"].id
  }

  network {
    bridge = "vmbr1"
    tag    = var.vlans["lan"].id
  }
}

# NAS VM example
resource "proxmox_vm_qemu" "nas" {
  name        = "homelab-nas"
  target_node = local.management_nodes[0].name
  clone       = "debian-template"
  cores       = 4
  sockets     = 1
  memory      = 8192

  disk {
    size   = "${var.nas_disk_gb}G"
    storage = local.management_nodes[0].storage_pool
    type   = "scsi"
  }
}

# Placeholder module invocation for worker nodes
module "k3s_workers" {
  source = "./modules/k3s-node"

  nodes = local.compute_nodes
  vlans = var.vlans
}

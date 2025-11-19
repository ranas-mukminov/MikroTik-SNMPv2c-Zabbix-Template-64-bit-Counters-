variable "proxmox_api_url" {
  type        = string
  description = "Base URL of the Proxmox API"
}

variable "proxmox_token_id" {
  type        = string
  description = "API token ID"
}

variable "proxmox_token_secret" {
  type        = string
  description = "API token secret"
  sensitive   = true
}

variable "nodes" {
  description = "List of hypervisor nodes with resources"
  type = list(object({
    name        = string
    host        = string
    cpu_cores   = number
    memory_gb   = number
    management  = bool
    storage_pool = string
  }))
}

variable "vlans" {
  description = "VLAN IDs and CIDRs"
  type = map(object({
    id   = number
    cidr = string
  }))
}

variable "nas_disk_gb" {
  type        = number
  default     = 512
  description = "Size of the NAS virtual disk"
}

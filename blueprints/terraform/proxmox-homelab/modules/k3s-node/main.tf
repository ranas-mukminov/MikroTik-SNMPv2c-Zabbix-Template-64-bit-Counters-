variable "nodes" {
  type = list(object({
    name      = string
    host      = string
    cpu_cores = number
    memory_gb = number
  }))
}

variable "vlans" {
  type = map(object({
    id   = number
    cidr = string
  }))
}

output "node_names" {
  value = [for node in var.nodes : node.name]
}

output "management_nodes" {
  value       = local.management_nodes
  description = "Nodes hosting management services"
}

output "k3s_worker_names" {
  value       = module.k3s_workers.node_names
  description = "K3s worker node names"
}

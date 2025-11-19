output "git_url" {
  value       = "https://${var.git_service.hostname}"
  description = "URL of the Git service"
}

output "monitoring_namespace" {
  value       = kubernetes_namespace.monitoring.metadata[0].name
  description = "Namespace hosting Prometheus/Grafana"
}

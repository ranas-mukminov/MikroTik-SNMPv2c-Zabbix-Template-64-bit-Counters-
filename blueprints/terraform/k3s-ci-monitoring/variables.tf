variable "kubeconfig_path" {
  type        = string
  description = "Path to the kubeconfig for the K3s cluster"
  default     = "~/.kube/config"
}

variable "git_service" {
  description = "Git service configuration"
  type = object({
    hostname = string
    admin_email = string
  })
  default = {
    hostname   = "gitea.local"
    admin_email = "git-admin@example.com"
  }
}

variable "monitoring_namespace" {
  type        = string
  default     = "observability"
  description = "Namespace for Prometheus/Grafana"
}

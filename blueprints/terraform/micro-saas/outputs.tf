output "public_domain" {
  value       = var.domain
  description = "Domain serving the SaaS"
}

output "backup_bucket" {
  value       = var.backup_bucket
  description = "Object storage bucket for backups"
}

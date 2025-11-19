variable "domain" {
  type        = string
  description = "Public domain for the SaaS"
}

variable "image_tag" {
  type        = string
  default     = "latest"
  description = "Application image tag"
}

variable "postgres_password" {
  type        = string
  description = "Database password"
  sensitive   = true
}

variable "backup_bucket" {
  type        = string
  description = "S3-compatible bucket for backups"
}

provider "docker" {}

resource "docker_network" "public" {
  name = "micro-saas-public"
}

resource "docker_image" "app" {
  name = "ghcr.io/run-as-daemon/micro-saas:${var.image_tag}"
}

resource "docker_image" "postgres" {
  name = "postgres:15"
}

resource "docker_container" "db" {
  name  = "micro-saas-db"
  image = docker_image.postgres.name
  env = [
    "POSTGRES_PASSWORD=${var.postgres_password}"
  ]
  networks_advanced {
    name = docker_network.public.name
  }
}

resource "docker_container" "app" {
  name  = "micro-saas-app"
  image = docker_image.app.name
  depends_on = [docker_container.db]
  env = [
    "DATABASE_URL=postgres://postgres:${var.postgres_password}@${docker_container.db.name}:5432/postgres"
  ]
  networks_advanced {
    name = docker_network.public.name
  }
}

resource "docker_container" "reverse_proxy" {
  name  = "micro-saas-proxy"
  image = "traefik:v2.10"
  command = [
    "--entrypoints.web.address=:80",
    "--entrypoints.websecure.address=:443",
    "--providers.docker=true",
    "--certificatesresolvers.acme.email=admin@${var.domain}",
    "--certificatesresolvers.acme.storage=/letsencrypt/acme.json",
    "--certificatesresolvers.acme.tlschallenge=true"
  ]
  volumes = [
    "/var/run/docker.sock:/var/run/docker.sock",
    "acme-data:/letsencrypt"
  ]
  networks_advanced {
    name = docker_network.public.name
  }
}

resource "docker_volume" "acme_data" {
  name = "acme-data"
}

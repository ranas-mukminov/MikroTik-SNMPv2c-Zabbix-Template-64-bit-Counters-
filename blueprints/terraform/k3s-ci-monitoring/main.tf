provider "kubernetes" {
  config_path = var.kubeconfig_path
}

provider "helm" {
  kubernetes {
    config_path = var.kubeconfig_path
  }
}

resource "kubernetes_namespace" "monitoring" {
  metadata {
    name = var.monitoring_namespace
  }
}

resource "kubernetes_namespace" "git" {
  metadata {
    name = "git-services"
  }
}

resource "helm_release" "gitea" {
  name       = "gitea"
  namespace  = kubernetes_namespace.git.metadata[0].name
  repository = "https://dl.gitea.io/charts/"
  chart      = "gitea"

  set {
    name  = "ingress.enabled"
    value = true
  }

  set {
    name  = "ingress.hosts[0].host"
    value = var.git_service.hostname
  }
}

resource "helm_release" "prometheus" {
  name       = "kube-prom"
  namespace  = kubernetes_namespace.monitoring.metadata[0].name
  repository = "https://prometheus-community.github.io/helm-charts"
  chart      = "kube-prometheus-stack"
}

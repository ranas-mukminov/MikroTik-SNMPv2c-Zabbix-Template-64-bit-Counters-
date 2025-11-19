# K3s CI/Monitoring blueprint

Deploys namespaces and Helm releases for a Git service and the kube-prometheus-stack on an existing K3s/Kubernetes cluster.

## Workflow

1. Point `kubeconfig_path` to your cluster.
2. Customize the Git hostname and namespace names in `variables.tf` or via `terraform.tfvars`.
3. Initialize Terraform with remote state.
4. Apply and follow the ingress instructions printed by the Helm charts.

Use the Ansible `k3s-node` role to bootstrap the underlying nodes before applying this blueprint.

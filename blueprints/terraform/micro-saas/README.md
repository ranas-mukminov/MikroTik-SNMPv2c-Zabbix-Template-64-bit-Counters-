# Micro-SaaS blueprint

Provisions a Traefik reverse proxy, application container, and PostgreSQL database using the Docker provider. Intended for edge servers or lightweight VPS environments.

## Steps

1. Set the `domain`, `image_tag`, and secrets in `terraform.tfvars`.
2. Configure DNS for the public domain to point at your host.
3. Run `terraform init`, optionally configuring remote state.
4. Apply; Traefik will request certificates automatically.
5. Schedule backups with the `blueprints/ansible/playbooks/micro-saas.yaml` playbook.

Extend the blueprint with object-storage sync, external monitoring, or off-site backup jobs as needed.

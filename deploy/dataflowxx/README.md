# dataflowxx Official Deployment

This folder defines the recommended production shape for `https://dataflowxx.dpdns.org`.

`dataflowxx.dpdns.org` is the official control plane, cloud service entry, and customer subdomain coordinator.

## Product Structure

- `/`
  Official homepage and brand entry.
- `/app/`
  The real PyMD web application.
- `/api/*`
  The Python backend used by the app.
- GitHub Pages
  Demo, docs, and release entry only.

## Goal

- Make `dataflowxx.dpdns.org` the official service entrance
- Keep GitHub Pages as the demo and lightweight fallback
- Assign customer HTTPS subdomains for vLAN/self-hosted deployments
- Use the same backend contract for official cloud and customer subdomain deployments

## Start The Backend

```bash
docker compose -f deploy/dataflowxx/docker-compose.yml up -d --build
```

## Reverse Proxy Expectation

The recommended proxy behavior is:

- serve the branded homepage at `/`
- reverse proxy `/app/*` to the PyMD app container
- reverse proxy `/api/*` to the same PyMD backend
- terminate HTTPS at the proxy

See:

- [docker-compose.yml](docker-compose.yml)
- [Caddyfile.example](Caddyfile.example)

## Validation Targets

After deployment, verify:

- `https://dataflowxx.dpdns.org/` shows the official homepage
- `https://dataflowxx.dpdns.org/app/` opens the PyMD app
- `https://dataflowxx.dpdns.org/api/health` returns `deployment_mode: cloud`
- the app can browse files and perform backend PDF conversions

## Recommended Split

- `dataflowxx.dpdns.org`
  Official product, cloud backend, control plane, and customer subdomain coordination
- `customer-a.dataflowxx.dpdns.org`
  Customer vLAN/self-hosted deployment assigned by Dataflowxx
- GitHub Pages
  Demo / lite mode / docs
- customer-owned domain
  Advanced customer-managed option using the same backend API

Customer deployment templates:

- [../customer-subdomain](../customer-subdomain)

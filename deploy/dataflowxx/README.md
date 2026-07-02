# dataflowxx Official Deployment

This folder defines the recommended production shape for `https://dataflowxx.dpdns.org`.

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
- Use the same backend contract for official cloud and customer self-hosted deployments

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
  Official product and backend
- GitHub Pages
  Demo / lite mode / docs
- customer domain
  Same backend API on customer infrastructure

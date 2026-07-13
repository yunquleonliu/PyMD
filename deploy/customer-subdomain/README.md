# PyMD Customer Subdomain Deployment

This is the recommended customer self-hosted shape.

The product team assigns a customer-specific HTTPS name, for example:

```text
https://customer-a.dataflowxx.dpdns.org
```

The customer does not need to buy or manage a public domain. Their network only needs to route that name to the PyMD server by one of the supported access patterns below.

## Target Shape

- PyMD backend runs inside the customer vLAN.
- Users open a HTTPS customer subdomain, not a raw `10.x.x.x:8765` URL.
- Browser `Open Folder` remains available because the page is loaded from a secure context.
- Customer data stays on customer infrastructure unless an explicit cloud sync or relay feature is enabled.
- `https://dataflowxx.dpdns.org` remains the official control plane, cloud service, and demo entry.

## Access Patterns

### Pattern A: Internal DNS

Use this when customer devices are inside the same vLAN/VPN.

1. Assign a subdomain, for example `customer-a.dataflowxx.dpdns.org`.
2. Customer internal DNS resolves that name to the PyMD server IP, for example `10.0.0.210`.
3. Install the TLS certificate/key provisioned for the assigned subdomain, or use a DNS-challenge automation path managed by Dataflowxx.
4. Reverse proxy HTTPS traffic to the PyMD backend on `127.0.0.1:8765`.

This is the preferred enterprise path when customer networking allows internal DNS.

Use [Caddyfile.internal-dns.example](Caddyfile.internal-dns.example) for this path. It expects certificate paths from `.env`.

### Pattern B: Managed Tunnel

Use this when internal DNS is difficult or remote access is needed.

1. Assign a subdomain, for example `customer-a.dataflowxx.dpdns.org`.
2. Run a tunnel agent on the customer server.
3. The public subdomain terminates HTTPS at the tunnel/provider edge.
4. The tunnel forwards traffic to `http://127.0.0.1:8765` inside the customer vLAN.

This keeps the backend off the public internet while still giving users a HTTPS product URL.

Use [Caddyfile.tunnel-origin.example](Caddyfile.tunnel-origin.example) for this path when the tunnel/provider terminates HTTPS and forwards to a local HTTP origin.

### Pattern C: Customer-Owned Domain

If the customer wants their own domain, they manage DNS and certificates themselves. PyMD still uses the same backend API and reverse proxy layout.

## Start Backend

```bash
docker compose --env-file .env -f deploy/customer-subdomain/docker-compose.yml up -d --build
```

## Validate

Open:

```text
https://customer-a.dataflowxx.dpdns.org/api/health
```

Expected:

```json
{
  "status": "ok",
  "deployment_mode": "self_hosted",
  "features": {
    "pdf_to_word": true,
    "pdf_to_excel": true,
    "pdf_to_ppt": true
  }
}
```

Then open the app URL and verify:

- `Open Folder` is visible and usable in Chrome/Edge.
- `.md` and `.pdf` files appear after choosing a local folder.
- PDF to Word/Excel/PowerPoint uses the backend.
- Backend selector can use `Custom server` with the assigned HTTPS URL.

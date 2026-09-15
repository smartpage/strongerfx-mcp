# MemeFX for your AI editor

Find a sound, retrieve its WAV file, and hand it to your editing workflow. The member MCP uses the same membership and API key as the website: $3/month, with no monthly download credits.

## Status

The authenticated adapter is implemented locally. Production API-key controls, member authentication configuration and distributable library still need launch verification. Do not advertise this as a tested live paid service yet. The separate reference MCP only returns metadata.

## Connect

Install dependencies with `npm ci --ignore-scripts`. Configure your MCP client using an absolute path to this checkout and your member key:

```json
{
  "mcpServers": {
    "memefx": {
      "command": "node",
      "args": ["/absolute/path/strongerfx/src/member-mcp.js"],
      "env": {
        "MEMEFX_API_KEY": "YOUR_MEMBER_API_KEY"
      }
    }
  }
}
```

Store the key in your client's secret configuration where supported. Never put it in prompts, public repositories or shared screenshots. Revoking a key or losing paid membership prevents further downloads.

## Tools

- `search_sounds`: query by name; maximum 50 results per call.
- `download_sound`: exact ID from search; returns WAV bytes as an embedded MCP resource. Your client/editor must support saving or importing that resource. The adapter does not modify your files or timeline automatically.

Example: “Search for a short reaction sound, download the selected WAV and import it into this edit.” The editing client supplies the import capability.

## HTTP API

Send `Authorization: Bearer YOUR_MEMBER_API_KEY`:

- `GET /api/membership/library`: available member sound IDs, names and durations.
- `GET /api/membership/download/{id}`: actual WAV bytes.

Account sessions manage keys through GET/POST `/api/membership/keys` and POST `/api/membership/keys/{id}/revoke`. API keys cannot create more keys or manage billing.

401: invalid/revoked credentials. 403: inactive paid membership. 404: unavailable sound. 503: temporary server/configuration failure.

No monthly quota is imposed. Each MCP delivery is limited to 20 MB to bound message size. This technical limit is not a credit system. Downloads are checked against the available distributable catalog. A membership does not change an asset's licence.

# MemeFX — find the sound you know

Search 44 curated sound references from five Reels. Find FAAH, Vine boom, Bruh and other labelled effects without searching through each video manually.

For developers building AI video editors, n8n workflows and sound research tools. Results include source Reel URLs, duration, category, sample rate, exact cut times, identity confidence notes and optional waveform peaks for rendering cards.

**This version returns metadata, not downloadable audio.** These reference recordings have unresolved redistribution status. It does not measure current virality, scrape new Reels, recognize uploaded audio, or include the $3/month consumer membership. Some identities remain unverified.

## MCP

Requires Node.js 22+. Run `npm ci --ignore-scripts`, then configure your MCP client:

```json
{"mcpServers":{"memefx":{"command":"node","args":["/absolute/path/strongerfx/src/memefx-mcp.js"]}}}
```

Tools: `search_meme_sounds`, `get_meme_sound`, `list_meme_categories`. Resource: `memefx://catalog`.

Example: “Find Vine boom references under two seconds and return their source links and waveforms.” The local stdio MCP is free and does not use Stripe keys or bill customers. Hosted paid MCP access is not implemented yet.

## Apify Actor

```json
{"query":"vine boom","limit":3,"includeWaveform":true}
```

Output is a dataset of matching reference records. Each result emits `sound-result` through the SDK's budget-aware `pushData`. No results means no result events; platform usage can still apply. Consult Store pricing before running. No price is activated by this repository.

Suggested pricing experiment: $0.001 per returned record ($1/1,000 results), subject to platform pricing requirements and measured runtime costs. This is a hypothesis, not validated market demand. With only 44 records, recurring value is limited; expand the catalog and validate repeat usage before scaling promotion.

The existing cloud Actor ID is `5QIecJdcPYf3tMcTe`; its previously built StrongerFX version is different from these local changes. A new build and publisher verification are required before releasing this version.

## Catalog maintenance

`npm run catalog:sync` imports metadata from the sibling website's `public/source-review/clips.json`. It never copies recordings, publishes local paths or converts unresolved rights into a download grant. Re-run after cuts change. Waveform values represent the actual clips.

`npm test` validates search, source parity and the real MCP handshake. `npm start` runs the Actor locally. Use an isolated `CRAWLEE_STORAGE_DIR` when testing billing events.

The legacy 254-effect CC0 implementation remains available via `npm run legacy:mcp` and `npm run legacy:actor`; it is separate from these 44 meme references.

Code is MIT. A code licence is not an audio licence. Contact: memefx@intuitiva.pt.

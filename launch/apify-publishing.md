# MemeFX update — 9 September 2026

Local version 2 now uses the actual 44-record MemeFX reference catalog. See `../MEMEFX.md`. Event changed to `sound-result`; output is metadata, not audio. No cloud deployment or pricing change has been made for version 2. Previous cloud success below applies only to the legacy build.

Release steps: validate publisher/payout status; deploy version 2 privately; test input/output and billing budget in cloud; configure the new event and an explicit price; update Store name/description; publish only after matching listing claims to available delivery. Proposed price experiment is $0.001/result, pending cost measurement.

# StrongerFX Actor publishing

Actor ID: 5QIecJdcPYf3tMcTe
Console: https://console.apify.com/actors/5QIecJdcPYf3tMcTe
Current slug: mentoring_baguette/strongerfx-mcp
Public source: https://github.com/smartpage/strongerfx-mcp

Paid publishing is blocked by missing publisher beneficiary/payout details. The account must supply its own legal details and payout destination and complete the requested verification. The public JM profile was enabled with a StrongerFX bio; contact email remains hidden.

Proposed starting price: USD 0.01 per delivered sound, billed by event `sound-delivered`. No actor-start event is emitted. Code uses Apify SDK `Actor.pushData(row, 'sound-delivered')` and respects the run charge limit. Pricing is NOT activated merely by this code. Configure the event in Publishing > Monetization after the account setup is complete; verify current pricing limits before activating it.

Maximum input limit is 50. Search, category and duration filtering available. WAV and MP3. Each dataset result includes the selected audio's base64 bytes, public download URL, preview URL, provenance and SHA-256 checksums. Consumers should decode bytes with code, not paste large base64 values into their LLM context.

The public repository offers the CC0 source files free. The paid Actor sells hosted search and delivery convenience. State this transparently in the Store listing.

Validation: initial cloud build and cloud run succeeded. Test payment limits after monetization is configured; live billing has not been tested.

Icon upload requires the browser extension's Allow access to file URLs permission, or user upload of assets/strongerfx-cover.jpg.

# MemeFX sound downloads for AI editors

Search by name or request exact IDs. Each result contains a WAV download link, duration, file size and SHA-256 checksum. Files are stored in the run's Apify key-value store; save them before the run storage expires or is deleted.

The Actor returns the available downloadable library, not every public preview on the MemeFX website. It does not guarantee increased reach or virality.

## Input

`query`: sound-name keywords; empty browses the library. `ids`: optional exact IDs. `maxDuration`: optional maximum seconds. `limit`: 1–50 files, default 10.

## Billing

The code emits `sound-delivered` only after a WAV is retrieved and stored. No result charge for empty searches or failed retrievals. The configured Apify listing controls actual prices and any platform/start charges. Monetization is not activated by this source code.

## Publisher setup — not customer input

Set the publisher-managed `MEMEFX_API_KEY` as a secret environment variable. It must access the available distributable library; never place it in Actor input, output or source. Customers pay through Apify and do not supply a second MemeFX membership key.

Release still requires provisioning that credential, a cloud delivery run, verifying charge-limit behavior, account beneficiary verification and configuring actual pricing. Local tests do not prove those steps completed. The old metadata-only implementation remains available through `npm run actor:references` for internal reference work.

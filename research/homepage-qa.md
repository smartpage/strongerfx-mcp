# Homepage QA — 9 September 2026

Browser initially showed a blank preview despite HTTP 200. Root cause: preview was inside production data providers. Moved preview selection to main.tsx so the local preview renders independently. Production remains unchanged unless the explicit preview environment flag is set.

Verified in browser: English hook, ten cards, $3/month offer and disabled checkout render. Searching dexter leaves the Dexter Meme card. Clicking its play control changes it to Pause with aria-pressed=true. This verifies playback initiation, not subjective audio quality or exact boundaries.

Fixed stale async playback state when switching rapidly; unmount pauses audio. Matching meme art and audio verification remain incomplete. No conversion or revenue claim follows from these checks.

# Apify audio comparison — checked 9 September 2026

The marketplace already has adjacent audio products. This is not evidence of guaranteed demand for MemeFX.

- Instagram Music & Trending Audio Scraper: https://apify.com/seemuapps/instagram-music-scraper — listing starts at $8 per 1,000 tracks; returns track metadata, Reel usage counts, trends and audio links. Listing showed 123 total users and 41 monthly active users during this check. These are users, not verified paying customers.
- Freesound Scraper: https://apify.com/crawlerbros/freesound-scraper/input-schema — keyword/tag/uploader search, licence, duration and preview URLs. Adjacent to a general effects library, rather than curated recognisable meme cuts.
- Instagram Audio Scraper: https://apify.com/memo23/instagram-audio-scraper — sound metadata and associated Reels/audio URLs.
- Sound Effects Generator: https://apify.com/ahmedmulti74/sound-effects-generator — marked deprecated. Do not use its listed price to justify active market demand.

## Product decision

Keep the website/API/MCP membership at the user's $3/month unlimited offer. Apify is a separate pay-per-delivery distribution channel. Suggested initial experiment remains $0.005 per successfully delivered audio file ($5/1,000); it is a proposal, not a configured live price or a demonstrated profitable rate. Measure actual compute/storage/transfer costs before activation.

Do not bill a metadata-only row as an audio download. The current v2 local Actor returns reference metadata; it needs actual approved audio delivery before that offer is accurate. No change to live pricing was made in this check.

Apify supports custom pay-per-event billing: https://docs.apify.com/actors/publishing/monetize and https://docs.apify.com/actors/monetize/set-up-monetization . Verify Actor-start event configuration as well as custom delivery events so the listing accurately describes all charges. Publish only after cloud run, delivery and charge-limit behavior are verified and account beneficiary setup is complete.

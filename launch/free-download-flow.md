# MemeFX free-download funnel — 2026-09-09

Current direct user offer: one free download after email login, then USD 3 per month per user for all available downloads. This supersedes the earlier $3/$7 bundles.

## Implementation
- `/free` uses the same homepage component with explicit free copy and sign-in form before the preview collection.
- Free login uses single-use email token and HTTP-only session cookie, no card/Stripe dependency.
- One normalized email can choose one sound atomically; same sound can be downloaded again. Other sounds require paid access.
- Private downloadable catalog `member-assets/catalog.json` currently contains Original Bass Drop, procedurally created, clearly labelled.
- The 44 extracted meme references remain a separate preview catalog with unresolved redistribution status. Paid membership is not ready for sale.
- 22 backend tests passed, including concurrent free claims, token replay, cancellation, paid API keys and webhook validation; production frontend build passed.

## Manychat
- Account fb5563652 connected to @memefxsounds.
- Flow content20260909071805_894719.
- DM keyword `sounds` plus `soundfx` saved, case-insensitive.
- Published LIVE message offers the original free effect and previews; button `Get my free sound` targets https://strongerfx.intuitiva.app/free?utm_source=instagram&utm_medium=dm&utm_campaign=soundfx.
- Comment trigger disabled/incomplete: no Instagram posts; free plan requires a specific post. All/next-post scopes require upgrade.
- Recipient test requires sign-in to a separate account; switching to intuitiva.pt failed. No successful recipient test claimed.

## Deployment
- d0f2ba7 contains free flow; a20ddd6 adds player mute control.
- First deployment rolled back because multiline Firebase credential broke dotenv serialization; compact JSON corrected that config.
- Production deployment 41495c9 finished. Access and billing now persist on dedicated SQLite volume /app/member-data, removing the shared Firestore quota dependency.
- Actual catch@intuitiva.pt email delivery, single-use login, free selection and browser reload persistence verified. Volume persistence verified through the billing deployment. Download button fetched the asset and saved the entitlement; browser download event timed out, so file-on-disk completion is still under verification.
- Production free session/email/SQLite env provisioned; paid flags remain false.
- Anonymous download returns401; private member-assets path returns404.
- Reel uploaded in original Instagram composer, full9:16 with audio on and caption prepared. Not published yet. Browser session disconnected; original composer recovery in progress.
- Stripe dedicated restricted key requires user's authenticator step. Other task owns billing; no paid purchase has been made.

## Latest browser/download hardening
- 3c526fe replaces fetch/blob synthetic clicks with native authenticated WAV links and browser Content-Disposition handling. Frontend build and TSX compilation passed. Deployment spjov545p1wmopstvsn74dg7 finished at 09:29:40 UTC; fresh production browser tab verified native authenticated WAV link and saved free entitlement.
- Native Chrome currently exposes an inaccessible Save dialog. User asked to save/dismiss so prepared Reel publication can continue. Original prepared composer tab1228938804 retained; no Reel published.
- Manychat Basic Builder verified LIVE/Saved, active DM keywords sounds,soundfx, new free-offer text. Comment trigger incomplete; recipient test still pending a separate Instagram login.

## Recipient verification — 2026-09-09 15:58 Lisbon
- Sent `soundfx` from signed-in user-owned @itsjohnmust to @memefxsounds; received the automatic reply. Manychat showed 1 run after the first test.
- Instagram web exposed reply text but no clickable button in the inspected conversation. Updated and published the message to include the full /free URL directly and Google/email login copy; a second keyword test received the exact updated text. Link clickability was not verified.
- Public @memefxsounds profile still shows 0 posts; comment trigger remains incomplete and comment-to-DM delivery is NOT tested.
- Other task owns current site deployment/domain migration to memefx.intuitiva.app. Update message origin after HTTPS deployment confirmation.

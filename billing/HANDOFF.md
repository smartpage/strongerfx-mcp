# Current billing status — 10 September 2026

Created active live price `price_1UDvUCK3CXqlfULuFAQfcgo4`: USD 399/month, product `prod_VE864LexZyP53X`. Updated local price configuration. No charge made.

Production container has no Stripe secret, price, webhook secret or portal configuration. Local restricted live key remains in gitignored `.env.membership.local`; it can create prices but customer-read and webhook-read return permission errors. Stripe dashboard currently requires user sign-in. Need Customers read/write, Subscriptions and Invoices read, Checkout Sessions read/write, Customer Portal write and Webhook Endpoints read/write. No test key is configured or test-mode purchase verified.

Added account-owned checkout confirmation route: verify Stripe session, paid invoice and active matching subscription before replacing the free session with a paid session. Checkout now returns to the account page. Automated tests verify unpaid and foreign checkout rejection, paid download/API access and cancellation revocation. 30 access/billing tests passed. Changes are local, not deployed. Sales remain closed pending actual Stripe permission/configuration and end-to-end payment verification.

## Previous handoff (historical)

# MemeFX billing handoff — 9 September 2026

Verified Stripe price: price_1UDfqRK3CXqlfULuL6AtKZlN, USD 300 cents per month. Product: prod_VE864LexZyP53X.

Existing restricted key is in strongerfx-site/.env.membership.local (gitignored). Do not print or commit it. Fresh API checks returned 403 for Customers, Subscriptions and Webhook Endpoints. The new MemeFX key was not created; user verification is pending. Dashboard tab was left open.

Required dedicated restricted-key permissions:
- READ: Customers, Products, Prices, Subscriptions, Invoices.
- WRITE: Checkout Sessions, Customer Portal, Webhook Endpoints/Event Destinations.

Then: save key through secret configuration, configure cancellation/payment-method portal, register signed webhook, provision server secrets, test sandbox purchase through email and actual download, deploy coordinated code, and only then enable sales. Live payment has not been tested. Never store credentials in this document.

Commercial instructions in this task: $3/month paid upfront, unlimited website/API/MCP usage; Apify priced separately per sound delivery. A coordinating task is implementing latest signup/free-download instructions and owns shared site files. Reconcile current offer across tasks before opening checkout.

Production a447494 is deployed; health and membership status return JSON, 44 preview WAV headers verified. Preview files are public; protected member delivery and actual approved deliverable catalog still require completion. No revenue verified.

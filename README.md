# odoo-crm-force-sso

Controller-only Odoo 17 module. On a team CRM host, an unauthenticated
`GET /web/login` with exactly one enabled OAuth provider 302s straight into that
provider's auth flow (LinkedTrust) instead of rendering the email+password form.

Load it via `server_wide_modules` in `odoo.conf` so it applies to **every**
database this Odoo serves — current teams and any new `crm-<slug>` — with no
per-database install. It defines no models, so server-wide loading is safe on
databases where it is not installed.

Escape hatches: `/web/login?no_autologin=1` and any `oauth_error` on the URL both
render the normal form (no redirect loop).

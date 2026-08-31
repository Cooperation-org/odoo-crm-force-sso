# -*- coding: utf-8 -*-
{
    "name": "CRM Force SSO",
    "version": "17.0.1.0.0",
    "summary": "Team CRM hosts go straight to LinkedTrust SSO — no password form.",
    "description": """
CRM Force SSO
=============

On a team CRM host (``crm-<slug>.workers.vc``) an unauthenticated visit to
``/web/login`` should never show the email+password form — it should go
straight to the single enabled OAuth provider (LinkedTrust). If the LinkedTrust
IdP cookie is already set (the person signed in at the dashboard), the provider
returns silently and the browser lands back in Odoo signed in, with no pause.
Elm, which shares the host and reuses the Odoo ``session_id`` cookie, then
renders elm-over-Odoo for the org.

This is a **controller-only** module (no models, no data). It is meant to be
loaded via Odoo's ``server_wide_modules`` so the redirect applies to *every*
database this Odoo serves — current teams and any new team created later —
without a per-database install. Because it defines no models, loading it
server-wide is safe for databases where it is not installed.

No core files are patched: it extends auth_oauth's ``OAuthLogin`` and reuses
``list_providers`` so the auth_link and OAuth ``state`` are built exactly as the
stock login buttons build them.

Escape hatches (so local login is never fully locked out):
  * ``/web/login?no_autologin=1`` always renders the normal form.
  * an ``oauth_error`` on the URL (a failed SSO round-trip) renders the form
    instead of bouncing again — no redirect loop.
""",
    "author": "Cooperation.org / LinkedTrust",
    "website": "https://github.com/Cooperation-org/odoo-crm-force-sso",
    "license": "LGPL-3",
    "category": "Extra Tools",
    "depends": ["auth_oauth"],
    "data": [],
    "installable": True,
    "application": False,
    "auto_install": False,
}

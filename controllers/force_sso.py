# -*- coding: utf-8 -*-
"""Force the Odoo login page straight to the single LinkedTrust provider.

Loaded server-wide (odoo.conf ``server_wide_modules``), so this override is
active for every database this Odoo serves — every current team CRM and any
new ``crm-<slug>`` created later — with no per-database install.
"""
from odoo import http
from odoo.http import request
from odoo.addons.auth_oauth.controllers.main import OAuthLogin


class OAuthLoginForceSSO(OAuthLogin):

    @http.route()
    def web_login(self, redirect=None, **kw):
        # Auto-jump only on a fresh GET, when nobody is signed in, when the
        # caller hasn't opted out (?no_autologin), when this isn't the bounce
        # back from a failed SSO round-trip (?oauth_error — would loop), and
        # only on databases that actually have the OAuth provider model.
        if (request.httprequest.method == "GET"
                and not request.session.uid
                and "no_autologin" not in kw
                and not kw.get("oauth_error")
                and "auth.oauth.provider" in request.env):
            # list_providers() signs each auth_link's OAuth state from
            # request.params['redirect'] — set our post-auth target there so
            # the browser comes back to it (default /web) with a session.
            request.params["redirect"] = redirect or "/web"
            providers = self.list_providers()
            if len(providers) == 1:
                # Odoo builds the OAuth redirect_uri from the request root,
                # which behind the gateway proxy comes out http even though the
                # public host is always https at the edge. Force the callback
                # scheme to https so it matches the IdP client registration
                # (registering http callbacks would be insecure).
                auth_link = providers[0]["auth_link"].replace(
                    "redirect_uri=http%3A%2F%2F", "redirect_uri=https%3A%2F%2F")
                return request.redirect(auth_link, code=302, local=False)
        return super().web_login(redirect=redirect, **kw)

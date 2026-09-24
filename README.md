# Agent OS Universal Capture

Public, sanitized distribution repository for the **Agent OS Universal Capture** Tampermonkey userscript.

## Install

Open the raw userscript URL:

`https://raw.githubusercontent.com/unwit1/universal-capture-plugin/main/agent-os-universal-capture.user.js`

Tampermonkey should offer to install or update it.

The script uses the same URL for `@updateURL` and `@downloadURL`, so after the one-time install, future versions committed here can be detected by Tampermonkey automatically. A GitHub Actions workflow also increments the userscript patch version whenever the script changes on `main`, so ordinary updates do not depend on someone remembering to bump `@version` manually.

## Supported capture adapters

- Reddit posts
- Amazon product pages
- YouTube videos
- Nexus Mods detail pages and listing cards
- SpaceBattles threads
- Questionable Questing threads
- Generic fallback for ordinary HTTP/HTTPS pages

## Privacy boundary

This repository is intentionally public and contains **only distributable browser code and documentation**.

It must never contain:

- Agent OS knowledge/profile data
- browsing history or saved captures
- endpoint credentials
- device tokens
- API keys or GitHub tokens
- employee/applicant/HR data
- personal email addresses, phone numbers, addresses, or local user paths
- private Agent OS configuration

The userscript stores its configured endpoint, device token, device label, and offline queue in Tampermonkey's per-browser storage. Those values are not committed here.

By default, if no endpoint is configured, captures are queued locally. The script has no analytics or telemetry service of its own.

See [PRIVACY.md](PRIVACY.md) for the audit model.

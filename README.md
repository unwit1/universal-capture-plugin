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
- Discord Web passive message indexing for messages that Discord renders while you browse, manually scroll, or view in Discord search results

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


## Discord passive indexing

On `discord.com/channels/...`, passive indexing defaults to **ON** the first time Discord is detected. If the user explicitly turns it off, that preference is preserved.

The userscript watches Discord's rendered message DOM and writes newly observed messages into a dedicated browser IndexedDB database named `agent_os_discord_index_v1`. It deduplicates by guild/channel/message ID and updates a record if the rendered message content changes. Rendered search-result messages are captured too, including results from channels other than the channel currently open when Discord provides a message permalink.

It does **not**:

- auto-scroll a channel;
- switch channels for you;
- extract the Discord authentication token;
- call Discord's private APIs;
- crawl channels that are not currently rendered in your browser.

A small `Discord Index ● <count>` indicator appears below the normal Agent OS button while Discord Web is open. Clicking it opens the built-in **local index browser**, where you can filter recent indexed messages, see whether a record came from a channel or search results, open the original Discord message, and export the current channel or complete local index as JSON.

The local archive is stored in browser-managed IndexedDB, not in a normal filesystem directory that a userscript can open. The index browser is the direct viewer for that storage. JSON exports are written through the browser's normal download flow.

Tampermonkey menu commands are available to:

- turn Discord passive indexing on/off;
- open the local Discord index browser;
- export the current channel's indexed messages as JSON;
- export the full local Discord index as JSON;
- clear the local Discord index.

The local Discord index persists across page reloads on that browser, but clearing Discord site data/browser storage can remove it.

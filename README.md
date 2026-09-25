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

By default, if no primary Agent OS endpoint is configured, captures are queued locally. A separately configured Google Sheet mirror can receive the same captures as a redundant activity log. The script has no analytics or telemetry service of its own.

See [PRIVACY.md](PRIVACY.md) for the audit model.


## Cross-site creator identity

Creator follow controls now participate in one provider-neutral identity layer instead of acting like unrelated per-site bookmarks. When the local Agent OS bridge supports creator profiles, a creator follow creates or updates a canonical creator profile containing confirmed accounts, strong aliases/handles, observed profile links, watch-target links, cross-provider discovery queries, and provenance.

The userscript captures strong account aliases and relevant external/profile links that are already visible on the page. Agent OS can use those signals to associate the same creator across YouTube, Nexus Mods, GitHub, Reddit, Patreon, Discord evidence, personal websites, and other supported surfaces. Exact account IDs/URLs are authoritative matches; unique high-confidence handle/alias matches and previously discovered profile links can associate another site with the existing creator profile.

Creator buttons query the local bridge for follow status. When the current account resolves to an already-followed creator, the control changes to a green `✓ Following` state rather than offering another independent follow. Discord performs this lookup lazily on hover to avoid issuing a large burst of requests for an entire member list.

Following a creator also requests deeper identity discovery. Agent OS stores search queries and desired source types for later enrichment and checks imported Discord messages for matching author aliases as identity candidates. Discord display-name matches remain candidates rather than silently becoming confirmed cross-site identities.

## YouTube creator-page follow

YouTube channel/creator pages now get an `AOS + Follow` button immediately beside the rendered channel name. It supports modern handle URLs such as `/@creator` as well as `/channel/...`, legacy `/c/...`, and `/user/...` routes, including their Videos, Shorts, Playlists, Community, and other tab views.

The follow record prefers YouTube's stable channel ID when the page exposes it and otherwise falls back to the creator route/handle. This keeps creator follows distinct from individual video captures while using the same Agent OS and Google Sheet mirror paths.

## YouTube video-title capture

YouTube video titles now get a compact `AOS +` button immediately to their right on supported rendered list surfaces such as Home, search results, subscriptions/recommendations, compact/sidebar videos, and playlist-style rows. The current watch-page title also gets the same control.

Clicking `AOS +` adds that specific video to Agent OS using the YouTube video ID, title, nearby channel name when available, canonical watch URL, thumbnail when available, and the page where the video was discovered. The same capture also follows the configured Google Sheet mirror path.

Buttons are keyed by video ID and reinjected idempotently as YouTube's SPA rerenders content, so repeated scans should not stack duplicate controls beside the same rendered title.

## Goodreads list capture

Goodreads list-style surfaces—including shelves, search/results pages, and rendered recommendation/list cards—get a compact `AOS +` button immediately to the right of each detected book title. A normal click saves that specific book to Agent OS using its Goodreads book ID, title, nearby author, book URL, cover image when available, and the source list/page where it was found. The same capture also uses the configured Google Sheet mirror.

Hold **Ctrl** or **Shift** while clicking `AOS +` to add the **entire Goodreads series** instead of only that book. The userscript resolves the series from the rendered row or book page, captures the Goodreads series as a series-level Agent OS item, and when possible enumerates the books shown on the Goodreads series page into the capture metadata. Meta/Command-click is accepted as the same shortcut on platforms that use it.

Whole-series additions are remembered in Tampermonkey storage. Other rendered books known to belong to that series change from `AOS +` to `AOS S✓`, including books identified from the captured series membership even when a list row does not expose a series link. A normal click on an `AOS S✓` button can still save that individual book separately.

The controls are idempotent across Goodreads dynamic rerenders, so rescanning the page does not stack duplicate buttons beside the same title.

## Discord follow controls

Discord's member list uses one compact Agent OS control per member row. Normal chat messages also get a tiny `+` immediately to the left of the visible author name; it appears only while the message/author is hovered or the control is focused. Clicking it follows that Discord user through the same Agent OS capture path and Google Sheet mirror.

Both controls are idempotent across Discord SPA rerenders. Member-list controls are keyed to Discord's stable member-row ID when available, while chat controls are keyed to the rendered message header and user identity when available. The script removes stale duplicate controls rather than injecting repeated buttons into usernames, activities, or message rows.

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


## Discord archive and compaction

Discord indexing now uses an incremental MutationObserver path: after the initial/route scan, it processes only newly added rendered message/search-result nodes instead of rescanning the complete rendered message list after every DOM mutation.

The local Discord database has two tiers:

- `messages`: active full records containing message text and metadata.
- `seen`: compact archive markers containing only the message identity, channel identity, timestamp, and archive time.

The built-in Discord Index browser has date-range controls. The intended workflow is:

1. Choose a From and/or Through date.
2. Click **Export date range**.
3. Verify the downloaded JSON archive exists.
4. Click **Compact exported range** using the same dates.
5. Full message bodies in that range are deleted from the active IndexedDB store and replaced by tiny `seen` markers.

If Discord later renders one of those archived messages again, the userscript checks the marker and does not store the full message again.

This makes the browser index useful as a rolling cache instead of requiring it to retain every historical message body forever.

Do not compact a range until its JSON export has been verified. The public userscript cannot reliably append silently to a permanent filesystem archive because browser userscripts are sandboxed from arbitrary filesystem writes. The long-term fully automatic design is to synchronize indexed records to the Agent OS local service, wait for a durable acknowledgement, and then compact acknowledged records automatically.


## Compact Discord archive format

Discord exports now use compact newline-delimited JSON and gzip when the browser supports `CompressionStream`.

Normal output:

    agent-os-discord-archive-...jsonl.gz

Fallback on browsers without gzip support:

    agent-os-discord-archive-...jsonl

The first JSONL line is a compact archive header containing the schema version, export metadata, field order, and dictionaries for guilds, channels, and authors. Every following line is one compact message row stored as an array rather than a verbose JSON object.

This avoids repeating property names, server names, channel names, author names, generated Discord message URLs, device labels, page titles, and other reconstructable/debug-only fields on every message.

Permanent rows keep only the data needed for the message library:

- Discord message ID
- channel ID
- author dictionary index
- timestamp as integer Unix seconds
- message text
- reply message ID when present
- non-redundant URLs
- attachment URL/label pairs
- whether the record came from rendered search results

The direct Discord message URL can always be reconstructed from guild/channel/message IDs.

After a successfully verified export, local archive markers are now reduced to essentially `{key}` only. Existing verbose markers are automatically rewritten into the smaller representation when the local IndexedDB schema upgrades to v3.


## Agent OS browser-control prototype

The userscript can optionally act as a bounded browser-side executor for the local Agent OS bridge. Browser control is **OFF by default** and must be enabled from the Tampermonkey menu with `Agent OS: Browser control ON/OFF`.

When enabled, each open page registers a short-lived browser session with the loopback bridge and polls for commands addressed to that session. The current prototype supports:

- page inspection and bounded text extraction;
- waiting for a CSS selector;
- clicking ordinary rendered controls;
- typing into ordinary non-sensitive fields;
- scrolling;
- HTTP/HTTPS navigation;
- history back/forward and reload;
- opening a new tab with Tampermonkey.

The executor intentionally does not provide arbitrary JavaScript execution. Password, payment-card, one-time-code, banking, SSN, and similar sensitive input fields are blocked. Clicks whose rendered control looks like a consequential action such as sending, submitting, publishing, deleting, purchasing, paying, transferring, or approving are returned as `approval_required` unless the caller explicitly resubmits the command after human approval.

The local bridge exposes live sessions and a durable command queue. Agent-facing clients use provider-neutral MCP tools such as `browser.sessions`, `browser.execute`, and `browser.command_status`; the userscript remains only the Firefox/Tampermonkey executor.

Because a userscript controls web-page DOM rather than Firefox chrome, this prototype does not automate Firefox settings, extension-management pages, native permission prompts, or arbitrary browser-profile UI. A future Firefox WebExtension can reuse the same Agent OS command protocol for those browser-level capabilities.

## Browser Interaction Journal

The userscript now includes a local-first Browser Journal for building future Agent OS context from ordinary browsing activity.

It records compact events for:

- page/navigation visits using a sanitized URL (origin + path; arbitrary query strings and fragments are not persisted);
- recognized search-query parameters such as `q`, `query`, and `search`;
- active page-session duration;
- finalized text entered into eligible text/search/email/URL/telephone fields, textareas, and contenteditable areas;
- copied page text;
- clicked links and their visible labels.

It does **not** record keydown/keyup events or save a character-by-character keystroke stream. Text is persisted only on blur, change, submit, route change, or page hide.

Sensitive-data protections exclude password and hidden inputs, payment-card/autocomplete fields, one-time-code/WebAuthn fields, fields whose labels indicate passwords, PINs, OTP/MFA/security codes, card/CVV/routing/account/SSN/API-key/token/private-key/secret data, and values that look like common private keys, GitHub/OpenAI/AWS/Google credentials, or JWTs. Text capture is also disabled on obvious login/auth/payment/security routes.

Browser Journal storage uses Tampermonkey's script-scoped storage in small per-tab chunks, so the journal is shared across websites without being tied to each website's IndexedDB origin. The floating `Journal ●` indicator is visible while journaling is active.

Tampermonkey menu commands can:

- turn Browser Journal on/off;
- include or exclude the current domain;
- export a date range as compact gzip-compressed JSONL;
- compact an already-exported Browser Journal range;
- export a combined Discord + Browser Journal activity archive while Discord Web is open;
- compact a verified combined range;
- clear the local Browser Journal buffer.

The combined export is intentionally run from Discord Web because Discord's local IndexedDB belongs to the Discord origin. The Browser Journal itself can be exported from any website.


## Per-thread / per-post save buttons

On SpaceBattles and Questionable Questing, Agent OS no longer uses one floating save button for the whole forum page. Instead, each rendered thread row gets its own `+ Agent OS` button on the right side of that thread entry. Individual thread pages also get an entity-scoped button near the thread title.

On Reddit, the same rule applies: the page-wide floating button is suppressed, and each rendered Reddit post/card gets its own `+ Agent OS` button. Individual post pages use the same post-scoped control.

This makes captures unambiguous: clicking a button always saves the specific thread/post attached to that button rather than the surrounding listing/feed page.


## Agent OS userscript update shortcut

A compact `AOS ↻` button is pinned to the top-right of pages where the userscript runs. Clicking it directly opens the latest public Agent OS `.user.js` URL so Tampermonkey can update or reinstall this userscript.

The permanent page button is intentionally scoped to Agent OS itself. Tampermonkey does not expose a userscript API that can enumerate every installed script and silently trigger an update-all operation, so the page no longer dedicates screen space to an ineffective "update all Tampermonkey scripts" shortcut.

The userscript menu still includes `Agent OS: Tampermonkey update help` for the manual all-scripts path (Tampermonkey toolbar icon → Dashboard → Utilities → Check for userscript updates) and `Agent OS: Update this userscript` for the same direct Agent OS update action.

## Google Sheet mirror

The userscript can mirror captures to a Google Apps Script endpoint backed by a Google Sheet while still sending the same data to the local Agent OS bridge.

Use the Tampermonkey menu commands:

- `Agent OS: Configure Google Sheet mirror`
- `Agent OS: Google Sheet mirror ON/OFF`
- `Agent OS: Sync Google Sheet mirror now`
- `Agent OS: Google Sheet mirror status`

The mirror is an independent outbox. Explicit page/post/thread/story/cart/follow captures are queued for the Sheet as soon as they are submitted. Browser Journal and Discord records that the local bridge durably acknowledges are also copied into the Sheet mirror outbox before browser-side compaction, so the Sheet can act as a secondary log without replacing Agent OS as the primary durable store.

Older installs that already use a `https://script.google.com/macros/s/.../exec` URL in the generic capture-endpoint setting remain compatible. When the local bridge is configured, that Apps Script URL is automatically treated as the Sheet mirror and the local bridge becomes the primary Agent OS capture destination.

Sheet endpoint URLs and optional tokens stay in Tampermonkey storage and are never committed to this public repository. Failed Sheet writes remain queued for retry instead of blocking or discarding the Agent OS capture.

## Local Agent OS bridge

The userscript can continuously drain its browser-side staging data into a local Personal Agent OS bridge.

Default batch endpoint:

    http://127.0.0.1:8766/api/v1/browser/batch

Default manual-capture endpoint:

    http://127.0.0.1:8766/api/v1/browser/capture

The bridge must be running locally and configured with its local token. The token is stored only in Tampermonkey script storage.

Use the Tampermonkey menu commands:

- `Agent OS: Configure local bridge`
- `Agent OS: Local bridge ON/OFF`
- `Agent OS: Sync local bridge now`
- `Agent OS: Local bridge status`

When configured, the userscript sends small batches automatically. Browser Journal events are removed from Tampermonkey storage only after the bridge responds with a durable acknowledgement. Discord messages are moved from the full IndexedDB message store into tiny seen markers only after the same durable acknowledgement.

This creates a bounded browser-side staging model:

    browser staging -> loopback bridge -> durable SQLite ACK -> local compaction

If the bridge is unavailable, times out, rejects the token, or fails to return a durable acknowledgement, the userscript keeps the local data and retries later.

Discord revisions are protected from an ACK race: before compacting an acknowledged Discord record, the userscript compares the current rendered-record fingerprint with the copy that was sent. If the message changed while the request was in flight, it stays in IndexedDB for a later sync.


## Fanfiction / web-fiction story capture

The userscript now adds per-story `+ Agent OS` controls on:

- FanFiction.net
- Archive of Our Own (AO3)
- Fiction.live

The generic page-wide floating button is suppressed on these sites.

On listing/search/browse pages, each rendered story/work entry gets its own button aligned with that specific entry. On an individual story/work page, the button is placed inline near the title.

Story captures use stable site-specific identities:

- FanFiction.net: story ID from `/s/<story-id>/...`
- AO3: work ID from `/works/<work-id>/...`
- Fiction.live: story ID from `/stories/<slug>/<story-id>/...`

The capture includes the canonical story URL plus best-effort story metadata available in the rendered page, such as title, author, summary/synopsis, fandoms, tags, chapter identity, and visible stats text. This lets Agent OS deduplicate the same story across chapters and list/detail views.


## Amazon per-item capture and cart import

Amazon now uses entity-scoped controls instead of the page-wide floating save button.

The userscript adds a `+ Agent OS` button to rendered Amazon product entries such as search results, supported recommendation/product cards, active cart rows, and the individual product page.

Per-item captures use the ASIN as the stable product identity and preserve best-effort rendered metadata including title, observed price, image, seller, availability, rating, Prime indicator, quantity when visible, selected variation text, marketplace, and source view.

On the Amazon cart page, an `Import Cart to Agent OS` control captures the currently rendered active cart as one structured `shopping_cart` snapshot. The snapshot contains the observed subtotal and an item array with each detected product's ASIN, title, quantity, price, seller, availability, variations, Prime state, image, and canonical product URL.

The cart snapshot uses a stable marketplace-specific source ID, so importing the cart again updates/deduplicates the current cart record through the Agent OS bridge rather than blindly multiplying identical cart captures. Individual cart products can still be saved separately with their own per-item buttons.

A Tampermonkey menu command, `Agent OS: Import Amazon cart`, provides the same cart import action when the cart page is open.

## Cross-site following

Version 3.13 adds first-class `follow_target` captures. Native page controls can send creators, users, individual videos, and projects to Agent OS with `intent: "follow"`, a stable source ID when the site exposes one, and provenance for where the target was discovered.

Current follow adapters include YouTube creators and individual videos, Nexus Mods authors, XenForo authors (including SpaceBattles and Questionable Questing), Patreon creators, GitHub repositories/projects, Reddit users, Discord users visible in rendered UI, plus lightweight creator/publication support for Twitch, Medium, Substack, Ko-fi, and itch.io. Discord falls back to a display-name identity when the rendered UI does not expose a stable numeric user ID, and marks that lower identity confidence for downstream reconciliation.

The intended Agent OS behavior is to treat these captures as durable watch definitions rather than ordinary bookmarks: resolve/deduplicate the entity, retain provenance, then let downstream follow/watch workers decide what constitutes meaningful new activity and how often to check it.

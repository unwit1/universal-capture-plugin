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

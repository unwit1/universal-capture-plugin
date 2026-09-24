# Browser Journal and combined activity archive format

## Browser Journal storage

The active Browser Journal is buffered in Tampermonkey script storage in small chunks. Each raw buffered event is a compact fixed-position array:

1. timestamp in milliseconds
2. event type integer
3. sanitized page URL
4. optional page title
5. optional field/context label
6. optional text
7. optional compact extra data

Event type order is:

- 0: page view
- 1: page session
- 2: finalized text
- 3: copied text
- 4: link click

The active buffer is temporary. After a verified archive export, a selected date range can be removed from Tampermonkey storage.

## Browser Journal archive

Exports are newline-delimited JSON and are gzip-compressed to `.jsonl.gz` when the browser supports CompressionStream.

The first line is a header with:

- archive schema/version;
- export time and count;
- event-type dictionary;
- page dictionary;
- field/context dictionary;
- fixed compact row field order.

Following lines are compact event arrays. Page URLs/titles and field contexts are dictionary encoded rather than repeated for every event.

## Combined activity bundle

When invoked from Discord Web, Agent OS can export one combined compressed bundle containing both the Discord archive stream and Browser Journal stream for the same requested date range.

The bundle begins with a top-level `agent-os-activity-bundle` header, then a stream marker for Discord followed by the normal compact Discord archive, then a stream marker for the Browser Journal followed by the compact browser archive.

The two streams remain independently parseable and can later be ingested into Agent OS as one chronological activity source.

## URL handling

Stored Browser Journal page URLs use only HTTP(S) origin + pathname. Arbitrary query strings and URL fragments are not persisted. Recognized search query values may be stored separately because they are useful intent/context signals.

## Text safety

The journal is not a keylogger. It does not persist keyboard events or intermediate per-character values. Text is finalized at lifecycle boundaries such as blur/change/submit.

Password, payment, OTP/MFA, security-code, credential/token/private-key and similarly sensitive fields/values are excluded by field metadata and content heuristics. Users can additionally exclude any current domain through the Tampermonkey menu.

# Discord archive format

The userscript exports Discord message libraries as compact JSONL, gzip-compressed when the browser supports the standard CompressionStream API.

## File extension

- `.jsonl.gz`: preferred gzip-compressed format
- `.jsonl`: fallback if browser-native gzip is unavailable

## Header line

The first line is one JSON object. Current schema version is `v: 1`.

Key fields:

- `k`: archive kind (`agent-os-discord-archive`)
- `e`: export time as Unix seconds
- `n`: message count
- `cols`: message-row field order
- `g`: guild ID -> guild name dictionary
- `c`: channel ID -> [guild ID, channel name] dictionary
- `a`: author display-name dictionary
- optional `from`, `to`, and `scope`

## Message rows

Every later line is one JSON array matching `cols`:

1. `m` - Discord message ID
2. `c` - channel ID
3. `a` - integer index into the author dictionary
4. `t` - Unix timestamp in seconds
5. `x` - message text
6. `r` - replied-to message ID or null
7. `u` - non-redundant URL array or null
8. `f` - attachment [URL, label] pairs or null
9. `s` - 1 when captured from rendered Discord search results, otherwise 0

The full Discord message URL is intentionally omitted because it is reconstructable from guild/channel/message IDs.

## Design goal

Files are append-friendly logical archive chunks rather than repeated full-library snapshots. Agent OS can treat the union of these chunks as one durable searchable library and deduplicate by Discord message ID.

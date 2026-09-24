# Privacy and public-distribution policy

This repository is a deliberately narrow public distribution surface for one browser userscript.

## What is public

The following are expected to be public:

- the userscript source code;
- supported-site adapter names and extraction logic;
- the repository owner's public GitHub username;
- commit timestamps and commit history;
- generic installation and configuration documentation.

## What must never be public here

Do not commit:

- real Agent OS capture payloads or browser history;
- personal profile or memory content;
- private project data;
- HR, applicant, employee, medical, financial, or other sensitive records;
- personal addresses, phone numbers, or email addresses;
- device-specific local filesystem paths;
- authentication cookies;
- GitHub personal access tokens;
- Agent OS device tokens;
- API keys, OAuth tokens, passwords, or private keys;
- private endpoint URLs containing identifiers or credentials.

## Runtime behavior

The userscript does not automatically upload browsing history.

A capture is created when the user invokes the Agent OS save action. If no endpoint is configured, the capture is queued in Tampermonkey storage on that browser.

When an endpoint is configured, the userscript sends the capture only to that configured endpoint. The endpoint and optional token are stored in Tampermonkey storage and are not part of the published source.

Tampermonkey may fetch the raw GitHub userscript URL to check for updates.

## Automated audit

`scripts/privacy_audit.py` is run by GitHub Actions on pushes and pull requests. It blocks a set of high-risk literal patterns such as private-key material, common token prefixes, credential-bearing URLs, obvious Windows user-profile paths, and common secret assignments.

Automated pattern scanning is defense in depth, not proof that a file contains no sensitive information. Public changes should still be reviewed before intentional publication.


## Discord Web local index

The Discord passive-indexing feature observes only message elements that Discord Web has rendered in the current browser session, including rendered Discord search results. Captured message records are stored locally in the browser's IndexedDB under the Discord origin. The feature defaults to on when Discord is first detected, but an explicit user choice to turn it off is persisted.

The public repository does not contain those records. The userscript does not embed a Discord token and does not use Discord's private message APIs. Clicking the Discord Index control opens an in-page browser for local IndexedDB records; it does not expose or open a browser-profile filesystem directory. Exporting the local index creates a JSON download only when the user explicitly invokes an export command.

Because message content can itself contain sensitive information, exported Discord index files should be treated as private data and must not be committed to this public repository.


## Discord archival compaction

Date-range archive exports contain the full selected Discord records and are therefore private user data. They are downloaded only after an explicit export action and must not be committed to this public repository.

After a user verifies an archive export, the userscript can compact that date range locally. Compaction removes full message bodies from the active IndexedDB `messages` store and retains only minimal `seen` markers needed to prevent the same rendered Discord message from being stored again. Clearing archive markers allows those messages to be indexed again if rendered later.

The userscript does not silently write a permanent archive to arbitrary local filesystem paths. Fully automatic durable archival should use an authenticated Agent OS local ingestion endpoint with acknowledgement before local compaction.


## Compact export contents

Compressed Discord archives still contain private message content even though they are storage-efficient. Compression and dictionary encoding reduce file size; they do not anonymize or encrypt the archive.

The compact export deliberately omits browser/device metadata and other reconstructable fields that are not required for the durable message library. Archive-marker compaction retains only the canonical message key needed to prevent re-indexing.

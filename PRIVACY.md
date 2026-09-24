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

The Discord passive-indexing feature observes only message elements that Discord Web has rendered in the current browser session. Captured message records are stored locally in the browser's IndexedDB under the Discord origin.

The public repository does not contain those records. The userscript does not embed a Discord token and does not use Discord's private message APIs. Exporting the local index creates a JSON download only when the user explicitly invokes an export command.

Because message content can itself contain sensitive information, exported Discord index files should be treated as private data and must not be committed to this public repository.

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".js", ".md", ".py", ".json", ".yml", ".yaml", ".txt"}

RULES = [
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("GitHub classic PAT", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("GitHub fine-grained PAT", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("OpenAI-style secret", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Windows user path", re.compile(r"(?i)\b[A-Z]:\\\\Users\\\\[^\\\\\r\n]+")),
    ("credential URL", re.compile(r"https?://[^/\s:@]+:[^@\s/]+@")),
    (
        "literal secret assignment",
        re.compile(
            r"""(?ix)
            \b(?:password|passwd|secret|api[_-]?key|access[_-]?token|device[_-]?token)
            \s*[:=]\s*
            ["'][^"'{}\s][^"']{7,}["']
            """
        ),
    ),
]

ALLOWLIST_SUBSTRINGS = {
    'settings.token = token.trim()',
    'settings.token ? "Device token saved locally."',
    'headers["X-Agent-OS-Token"] = settings.token',
    "X-Agent-OS-Token: <device token>",
}

problems: list[str] = []
for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in TEXT_SUFFIXES:
        continue
    text = path.read_text(encoding="utf-8", errors="replace")
    for label, pattern in RULES:
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            excerpt = match.group(0)
            if any(allowed in excerpt for allowed in ALLOWLIST_SUBSTRINGS):
                continue
            problems.append(f"{path.relative_to(ROOT)}:{line}: {label}: {excerpt[:120]!r}")

if problems:
    print("PRIVACY AUDIT FAILED")
    print("\n".join(problems))
    sys.exit(1)

print("Privacy audit passed: no blocked high-risk literal patterns found.")

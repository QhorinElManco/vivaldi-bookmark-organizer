# Chrome Bookmark Organizer — Extension (Phase 2)

> Status: **Not implemented yet.** This directory is a placeholder for the upcoming Chrome extension.

## Why an extension on top of the Skill

The Skill (in `../skill/`) edits the local `Bookmarks` JSON file directly. That works, but Chrome Sync overrides those edits if the user is signed in — see [`../docs/chrome-sync.md`](../docs/chrome-sync.md). The Skill mitigates this by guiding the user through manually toggling sync, but it's friction.

A Chrome extension calling `chrome.bookmarks` API has no such problem: the API goes through Chrome's own bookmark engine, which the sync system observes and propagates correctly.

## Planned design

- **Manifest V3** extension, browser-action popup.
- Permissions: `bookmarks`, `storage`. No host permissions.
- UI: tree view of current bookmarks → "Analyze" button → AI proposal panel → "Apply selected" with per-row toggles.
- AI backend: pluggable. Default to Claude API via user-supplied key (stored in `chrome.storage.local`); also support OpenAI-compatible endpoints.
- Same plan format as the Skill, so users can flow between the two.

## Contributing

Open an issue or PR. The Skill's `apply.py` logic should be portable to TypeScript with minimal effort — it's deliberately stateless and JSON-in/JSON-out.

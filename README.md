# Chrome Bookmark Organizer

AI-assisted reorganization of your Chrome (or any Chromium-based browser) bookmarks. You bring a messy `Bookmarks` file with hundreds of unsorted items; Claude proposes a category structure; you confirm; the tool applies it.

> Built after one too many "where did I save that link" moments.

## Components

| Path | Status | Description |
|---|---|---|
| [`skill/`](skill/) | ✅ Working | Claude Code skill. Wraps the analysis + apply workflow with AI categorization in the loop. |
| [`extension/`](extension/) | 🚧 Planned | Chrome extension using `chrome.bookmarks` API. Will sidestep the sync gotcha entirely. |

## Quick start (Skill)

### Install
Copy or symlink the `skill/` directory into your Claude Code skills folder:

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skill" ~/.claude/skills/chrome-bookmark-organizer
```

### Use
In Claude Code, just ask:

> 整理一下我的 Chrome 书签

> Help me organize my Chrome bookmarks

Claude will load the skill, walk through analysis, propose a categorization plan, and apply it after your approval.

### Standalone (without Claude Code)

The scripts work standalone too:

```bash
# Analyze
python3 skill/analyze.py
python3 skill/analyze.py --show-loose --top-domains 30

# Apply a plan you wrote yourself
python3 skill/apply.py ~/Library/Application\ Support/Google/Chrome/Default/Bookmarks plan.json --in-place
```

Plan format: see [`skill/SKILL.md`](skill/SKILL.md#4-build-plan-json) §4.

## ⚠️ Chrome Sync warning

If your Chrome is signed in and syncing, **disable sync before applying changes**. Otherwise Chrome will silently overwrite your local edits with the cloud version on next launch. Full explanation and workaround: [`docs/chrome-sync.md`](docs/chrome-sync.md).

The Skill detects this automatically and guides you through.

## Supported browsers

Anything based on Chromium uses the same `Bookmarks` JSON schema:

- Google Chrome ✅ tested
- Microsoft Edge — should work, path is `~/Library/Application Support/Microsoft Edge/Default/Bookmarks` on macOS
- Brave — `~/Library/Application Support/BraveSoftware/Brave-Browser/Default/Bookmarks`
- Opera, Vivaldi, Arc — likely work, untested

Pass the path explicitly via `python3 skill/analyze.py /path/to/Bookmarks`.

## Design principles

- **The user owns their data.** Every destructive action requires explicit confirmation. Backups are timestamped and never auto-deleted.
- **All or nothing.** If any plan entry fails, `apply.py` writes nothing and exits 2 — a half-applied reorganization is harder to recover from than none. `--allow-partial` opts out. A final invariant check refuses to write if any node would disappear other than through `delete_ids`.
- **Reuse existing structure.** If the user has hand-curated folders, those names are preserved; new buckets only appear when no existing folder fits.
- **Conservative bias.** When in doubt, leave it alone. Better one orphan loose bookmark than a wrong categorization.
- **Stateless tools, smart prompts.** The Python scripts are mechanical (read/write/validate). All the judgment calls (which folders, what's a duplicate) live in the SKILL.md prompt that Claude executes.

## License

[MIT](LICENSE)

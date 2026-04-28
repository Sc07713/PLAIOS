---
name: closing-out
description: Use when the user signals end of a PLAIOS session — "close out", "wrap up", "done for now", "let's stop here", or similar — to mirror Claude memory into the repo, commit the backup, and surface pending domain changes for explicit user approval before staging non-memory work.
---

# Closing Out a PLAIOS Session

## Purpose

PLAIOS state lives in two places: **Claude config memory** (`C:\Users\smckennie\.claude\projects\D--PLAIOS\memory\`) and the **PLAIOS repo** (`D:\PLAIOS\`). The config dir is local-only — if it's lost, every memory is lost. Close-out exists to ensure both are preserved in git.

## When to Use

User signals session end via phrases like:
- "close out" / "close it out" / "let's close out"
- "wrap up" / "wrap it up"
- "done for now" / "let's stop here"
- "save and close" / "commit and close"

When in doubt, ask: *"Want me to run close-out (mirror memory + commit pending domain work)?"*

## Procedure

**1. Mirror memory into the repo.**
```bash
cp -r /c/Users/smckennie/.claude/projects/D--PLAIOS/memory/. /d/PLAIOS/memory/
```
The repo's `memory/` is a snapshot, not the source of truth. Always overwrite from config dir.

**2. Run `git status` and surface pending work in groups.**
Group by intent so the user can approve granularly:
- Memory backup (always commit)
- Domain content updates (state files, manifests, references)
- New domain reference material (research docs, spreadsheets, data dumps)
- New domain drafts (e.g., travel/)
- Settings (`.claude/`, domain-level `.claude/`)

**3. Commit memory backup unconditionally.**
Scope: `memory/` only. Use `git add memory/` — never `git add -A`.

**4. Ask the user which other groups to commit.**
Don't blindly stage everything — the working tree may contain in-progress work, sensitive data, or large binaries the user hasn't validated. Show the groups, ask which to include.

**5. Commit approved groups in logical units.**
Match the existing commit-message convention from `git log`:
- `Domain: brief description` (e.g., `Finance state: …`, `PocketSmith: …`)
- HEREDOC for body, with `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>` trailer

**6. Do NOT push unless explicitly asked.**
Pushing is its own decision — the user will say "push" or "send to remote" when they want it.

## Red Flags — STOP

- About to `git add -A` or `git add .` — STOP, scope by group instead
- About to commit a binary (`*.xlsx`, `*.zip`) without flagging it — STOP, surface it
- About to `git push` without being asked — STOP, this is opt-in
- About to amend a previous commit — STOP, always create a new commit
- About to skip hooks (`--no-verify`) — STOP, fix the underlying issue

## Quick Reference

| Step | Command | Scope |
|------|---------|-------|
| Mirror | `cp -r ~/.claude/projects/D--PLAIOS/memory/. /d/PLAIOS/memory/` | All memory files |
| Stage memory | `git add memory/` | Memory only |
| Commit memory | `git commit -m "Memory: …"` | Memory only |
| Show domain status | `git status` | Read-only |
| Stage approved group | `git add <specific paths>` | User-approved scope |
| Push | (only if user says "push") | — |

## Notes

- The repo `memory/` is a **mirror**, not the live memory. Edits should still go to the Claude config dir; the mirror updates at close-out.
- If the user has done domain work mid-session that wasn't committed at the time, close-out is the catch-up moment.
- A close-out commit message like `Session close-out: …` is fine when the work spans domains and doesn't fit one topic.

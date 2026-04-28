---
name: Close-out protocol — back up memory to git
description: When user says "close out" or similar, sync memory dir into PLAIOS repo and commit, plus commit any pending domain changes
type: feedback
originSessionId: f2017cf2-e4e9-4673-9d0b-e9b1caa1bb99
---
When the user closes out a session (says "close out", "wrap up", "done for now"), run this protocol:

1. **Mirror memory into the repo.** Copy `C:\Users\smckennie\.claude\projects\D--PLAIOS\memory\*` into `D:\PLAIOS\memory\` so the Claude config memory is backed up in git.
2. **Check pending domain changes.** Run `git status`. Surface anything uncommitted under `domains/`.
3. **Commit.** Stage memory/ + any agreed domain changes. Use a clear close-out message describing what was decided in the session.
4. **Do not push** unless explicitly asked.

**Why:** User wants a safety net so the memory + state is preserved in git "just in case we lose everything." The Claude config dir is local-only and not backed up.

**How to apply:** Treat as standing instruction. When committing memory, scope additions to memory files only — do NOT blindly `git add -A` because the working tree may have binary spreadsheets, sensitive TSVs, or in-progress domain work the user hasn't validated. For non-memory changes, surface the list and ask what scope to include before committing.

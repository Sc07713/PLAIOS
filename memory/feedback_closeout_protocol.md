---
name: Close-out protocol — invoke closing-out skill
description: When user signals end of session (close out, wrap up, done for now), invoke the closing-out skill which mirrors memory to repo and commits with user-approved scope
type: feedback
originSessionId: f2017cf2-e4e9-4673-9d0b-e9b1caa1bb99
---
When the user signals session end ("close out", "wrap up", "done for now", "let's stop here"), invoke the **`closing-out`** skill (project skill at `D:\PLAIOS\.claude\skills\closing-out\SKILL.md`).

**Why:** User wants memory backed up to git "just in case we lose everything" and domain changes committed at the end of each working session. Captured as a skill so the procedure is invoked uniformly rather than reconstructed each time.

**How to apply:** On close-out signals, call the Skill tool with `closing-out`. Don't improvise the procedure — the skill is canonical. Don't `git push` unless the user explicitly says to.

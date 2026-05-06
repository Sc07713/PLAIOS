# bin/new-investigation.ps1
# Scaffold a new investigation folder under journal/investigations/.
# Usage (from PLAIOS root): .\bin\new-investigation.ps1 <topic-slug>

param(
    [Parameter(Mandatory=$true)]
    [string]$Slug
)

# Preflight: must run from PLAIOS root.
if (-not (Test-Path ".\AGENTS.md") -or -not (Test-Path ".\journal\investigations")) {
    Write-Error "Must be run from D:\PLAIOS\ (project root). AGENTS.md and journal/investigations/ must exist in the current directory."
    exit 1
}

# Slug validation: lowercase letters, digits, hyphens only.
if ($Slug -notmatch '^[a-z0-9-]+$') {
    Write-Error "Invalid slug '$Slug'. Must match [a-z0-9-]+ - lowercase letters, digits, hyphens only."
    exit 1
}

$Date = Get-Date -Format "yyyy-MM-dd"
$Folder = "journal/investigations/$Date-$Slug"

if (Test-Path $Folder) {
    Write-Error "Folder already exists: $Folder"
    exit 1
}

New-Item -ItemType Directory -Path $Folder | Out-Null

$Files = @(
    "00-topic.md"
    "01-questions-claude.md"
    "01-questions-codex.md"
    "01-questions-gemini.md"
    "02-consolidated-questions.md"
    "03-spec.md"
    "04-research-claude.md"
    "04-research-codex.md"
    "04-research-gemini.md"
    "05-research-pack.md"
    "06-deliberation-claude.md"
    "06-deliberation-codex.md"
    "06-deliberation-gemini.md"
    "06-deliberation.md"
    "07-disposition.md"
    "08-meta-reflection-claude.md"
    "08-meta-reflection-codex.md"
    "08-meta-reflection-gemini.md"
    "08-meta-reflection.md"
    "09-mediation-claude.md"
    "09-mediation-codex.md"
    "09-mediation-gemini.md"
    "09-resolution.md"
    "10-final-output.md"
)

foreach ($File in $Files) {
    New-Item -ItemType File -Path "$Folder/$File" | Out-Null
}

# Seed README.md with phase tracking.
# Single-quoted here-string for literal content; placeholders __SLUG__ / __DATE__ get replaced after.
$ReadmeTemplate = @'
# Investigation: __SLUG__

**Started:** __DATE__
**Phase:** 00 (topic intake)
**Status:** open
**Last touched:** __DATE__

## Topic summary

(1-2 sentences on what is being decided. Filled in as `00-topic.md` is written.)

## Convergence target

(What does a converged outcome look like for this investigation? E.g., "Decide which insurances to drop / replace / restructure, with a 1-page decision record at journal/decisions/.")

## Phase log

- __DATE__ - folder bootstrapped; phase 00 (topic intake) starts here.
'@

$Readme = $ReadmeTemplate -replace '__SLUG__', $Slug -replace '__DATE__', $Date

Set-Content -Path "$Folder/README.md" -Value $Readme -Encoding utf8

Write-Host "Created $Folder" -ForegroundColor Green
Write-Host "Next: edit 00-topic.md to capture topic + initiator goals + phase model."
Write-Host "Update README.md after each phase boundary so a cold-start reader knows where the investigation is."

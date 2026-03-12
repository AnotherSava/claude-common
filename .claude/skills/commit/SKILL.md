---
name: commit
description: Analyzes changes and generates Conventional Commit messages
allowed-tools: Read, Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git status:*), Bash(git log:*), Bash(git reset HEAD:*), Bash(git ls-files:*)
---

# Commit Changes

You are tasked with creating git commits for the changes made during this session.

## Bash rules

**One command per call.** Each Bash call must contain a single `git` command — no `&&`, `;`, or pipes. This is required for allowed-tools pattern matching. Use separate sequential Bash calls when commands depend on each other; use parallel calls for independent reads (e.g. `git status` and `git diff`).
```
BAD:  git add README.md && git commit -m "msg"
GOOD: Bash call 1: git add README.md
      Bash call 2: git commit -m "msg"
```

**No non-git commands.** Use git's own flags instead of piping to shell tools.
```
BAD:  git diff | wc -l
GOOD: git diff --stat
```

**No `cd`.** The working directory is already the project root.
```
BAD:  cd src && git status
GOOD: git status
```

## Process:

1. **Optimize imports in modified files**

2. **Update stale documentation and comments:**
   - Read the project README.md (at the repo root) and check if any references to changed paths, APIs, or behavior are stale
   - Check comments and docstrings in source files that reference changed behavior, not just the modified files themselves
   - Fix any stale references before proceeding — do not commit code with outdated docs

3. **Think about what changed:**
   - Review the conversation history and understand what was accomplished
   - Read `.gitignore` to know which files should be excluded
   - Run `git status` to see current changes
   - Run `git diff` for unstaged changes and `git diff --cached` for staged changes — review both
   - Include ALL uncommitted changes in the plan — both staged and unstaged — unless they match `.gitignore` patterns
   - Exclude any untracked files that match `.gitignore` patterns — do not propose committing them

3. **Plan your commit(s):**
   - Group into atomic commits by feature/fix/refactor, make sure that each element can be committed independently.
   - Identify which files belong together
   - Put tests and documentation changes in the same commit as the feature they cover, unless there is a significant reason to separate
   - Draft Conventional Commit messages (type: subject\n\nbody bullets)
   - Use imperative mood in commit messages
   - Subject line max 50 characters, body lines wrapped at 72 characters
   - Focus on why the changes were made, not just what

4. **Validate each commit message:**
   - Imperative mood ("add" not "added")
   - Subject line ≤ 50 characters
   - No trailing period
   - Type prefix not repeated in description (e.g. not "refactor: refactor...")
   - No capitalized first word after type prefix
   - Do not list files or file-level descriptions in the commit message body — the file list is shown separately in the plan

5. **Present your plan to the user:**
   - Separate each commit with a unicode line: `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`
   - For each commit show:
     1. **Commit N**
     2. Commit message with only the type prefix in **bold** (e.g. **refactor**: description), no code block
     3. Number of files and lines changed, then without an empty line in betweem, file list: each file as `inline code` followed by brief description. Pad each file entry with spaces so all entries match the length of the longest one, aligning descriptions into a column.
   - End with: "I plan to create **N** commit(s) with these changes. Shall I proceed?"

6. **Execute upon confirmation:**
   - First, run `git reset HEAD` to unstage everything — this ensures pre-staged files don't leak into the wrong commit
   - Use `git add` with specific files (never use `-A` or `.`)
   - Create commits with your planned messages using `git commit -S` to GPG-sign them
   - Show the result with `git log --oneline -n [number]`

## Important:
- **NEVER execute commits without explicit user approval.** Invoking `/commit` (even repeatedly) only requests a plan — it is NOT approval to proceed. Wait for a clear "yes", "proceed", or equivalent before running any `git commit` commands.
- **NEVER add co-author information or Claude attribution**
- Commits should be authored solely by the user
- Do not include any "Generated with Claude" messages
- Do not add "Co-Authored-By" lines
- Write commit messages as if the user wrote them

## Examples

Good output:
```
**Commit 1**

**chore**: simplify commit skill, remove script
- Drop format_files.py in favor of inline alignment
- Make skill portable for global use
- Add Claude Code skills section to README

3 files, +7/−35 lines
`.claude/skills/commit/SKILL.md`                  Remove script references, simplify formatting
`.claude/skills/commit/scripts/format_files.py`   Deleted
`README.md`                                       Add Claude Code skills section
```

Good commit messages:
- `feat: add marker holder model`
- `refactor: consolidate edge filtering logic in edgefilters module`
- `chore: update README with published models, add missing deps to requirements`
- `feat: add fillet radius reuse and arc support to Pencil`

Bad commit messages:
- `feat: added new marker holder model to the project` (past tense, verbose)
- `refactor: refactored edge filtering` (redundant — type already says refactor)
- `update stuff` (no type, vague)
- `fix: fix bug` (no useful information)
- `feat: add SmartBox.with_delta() class method and update all callers to use it` (too long, move details to body)
- `feat: add keepPathFrom site rule for path trimming` with body `Strips SEO slug segments before an anchor like dp or gp, producing cleaner Amazon URLs.` (body repeats what the subject already says — body should add context not visible from the diff, not rephrase the subject)

## Out of scope:
- Do NOT push to remote
- Do NOT amend existing commits
- Do NOT create or switch branches

## Remember:
- You have the full context of what was done in this session
- Group related changes together
- Keep commits focused and atomic when possible
- The user trusts your judgment - they asked you to commit

---
name: pr-update
description: Squash new local changes into a single commit and push to update an existing PR.
allowed-tools: Bash(git status:*), Bash(git log:*), Bash(git diff:*), Bash(git reset --soft:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git symbolic-ref:*), Bash(git rev-parse:*), Bash(git fetch:*), Bash(git rebase:*), Bash(gh pr view:*), Bash(gh pr edit:*), Read, Glob, Grep
---

# Update Existing PR

Squash all new local changes (uncommitted + unpushed commits) into a single Conventional Commit, push it to the remote branch, and update the PR description.

Read `~/.claude/skills/shared/bash-rules.md` for bash command constraints.

## Workflow

### Step 1: Gather context

1. Determine the main branch:
   ```
   git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||'
   ```
   Fall back to `main` if the command fails.

2. Get the current branch name and working tree status:
   ```
   git rev-parse --abbrev-ref HEAD
   git status
   ```
   Abort if on the main branch — there is no PR to update.

3. Verify a PR exists for this branch:
   ```
   gh pr view --json number,title,body,url
   ```
   Abort if no PR is found.

4. Fetch the latest remote state:
   ```
   git fetch origin main
   git fetch origin <branch-name>
   ```

5. Identify the boundary between already-pushed and new changes.
   The remote branch tip (`origin/<branch-name>`) is the baseline —
   everything after it is new. Collect:
   - Unpushed commits:
     ```
     git log origin/<branch-name>..HEAD --oneline
     ```
   - Unstaged and staged changes:
     ```
     git diff --stat
     git diff --cached --stat
     ```
   If there are no unpushed commits AND no uncommitted changes, abort —
   nothing to update.

6. Get the full diff of new changes for analysis:
   ```
   git diff origin/<branch-name>..HEAD --stat
   git diff origin/<branch-name>..HEAD
   git diff
   git diff --cached
   ```

### Step 2: Draft commit message

Read `~/.claude/skills/shared/commit-message-rules.md` for formatting and validation rules.

Compose a commit message for the **new changes only** (not the entire PR), following those rules. Analyze the diff and unpushed commit messages to write a meaningful summary.

### Step 3: Confirm with user

Display:
1. The drafted commit message
2. A summary of what will be added to the PR description

Ask the user to approve or revise. Do not proceed until confirmed.

### Step 4: Squash new changes into a single commit

1. Soft-reset to the remote branch tip to collapse unpushed commits:
   ```
   git reset --soft origin/<branch-name>
   ```

2. Stage everything (including any previously uncommitted changes):
   ```
   git add -A
   ```

3. Create the single GPG-signed commit:
   ```
   git commit -S -F - <<'EOF'
   <approved commit message>
   EOF
   ```

### Step 5: Rebase onto main

Ensure the branch is up to date with main:
```
git fetch origin main
git rebase main
```
If the rebase produces conflicts, stop and ask the user to resolve them.

### Step 6: Push

Push the updated branch. Since we squashed commits that were already on
the remote, force-with-lease is required:
```
git push origin <branch-name> --force-with-lease
```

### Step 7: Update PR description

1. Read the current PR body:
   ```
   gh pr view --json body
   ```

2. Append an "Update" section to the PR body with a summary of the new
   changes. Use a HEREDOC:
   ```
   gh pr edit --body "$(cat <<'EOF'
   <existing body>

   ## Update: <short description>
   <bullet points summarizing the new commit>
   EOF
   )"
   ```

3. Report the PR URL to the user.

## Important

- **NEVER proceed without explicit user approval** of the commit message
- Do NOT push to a different branch or create a new PR
- Do NOT amend the existing remote commits — only squash new local changes

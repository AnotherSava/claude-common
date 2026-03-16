# Bash Rules for Git/GH Skills

**One command per call.** Each Bash call must contain a single `git` or `gh` command — no `&&`, `;`, or pipes. This is required for allowed-tools pattern matching. Use separate sequential Bash calls when commands depend on each other; use parallel calls for independent reads (e.g. `git status` and `git diff`).
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

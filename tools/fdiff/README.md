# diff — File Comparison Tool

Compare files and directories with clear, colorized output. Essential for code reviews, debugging, and configuration management.

**Location:** `~/workspace/tools/diff/`

**Install:** Symlink to `~/.local/bin/diff`

```bash
ln -s ~/workspace/tools/diff/diff.py ~/.local/bin/diff
chmod +x ~/workspace/tools/diff/diff.py
```

## Features

- **File Comparison** — Compare two files line-by-line
- **Directory Comparison** — Compare directory contents
- **Multiple Formats** — Unified, context, and side-by-side diffs
- **Colorized Output** — Green for additions, red for deletions
- **String Comparison** — Compare text strings directly
- **Context Lines** — Configure how much context to show
- **Recursive Compare** — Compare directory trees
- **Summary Statistics** — Quick overview of differences

## Key Commands

### File Comparison

- `diff <file1> <file2>` — Compare two files (unified diff)
- `diff <file1> <file2> -c` — Context diff format
- `diff <file1> <file2> -s` — Side-by-side diff
- `diff <file1> <file2> --lines 5` — Show 5 lines of context
- `diff <file1> <file2> --no-color` — Disable colors

### Directory Comparison

- `diff <dir1> <dir2> --compare-dirs` — Compare directories
- `diff <dir1> <dir2> --compare-dirs -r` — Recursive compare

### String Comparison

- `diff --string "text1" "text2"` — Compare two strings

## Examples

### Basic File Comparison

```bash
# Compare two files
diff file1.txt file2.txt

# Compare Python files
diff script_old.py script_new.py

# Compare config files
diff config.production.yaml config.staging.yaml
```

### Different Diff Formats

```bash
# Unified diff (default)
diff file1.txt file2.txt

# Context diff
diff file1.txt file2.txt -c

# Side-by-side diff
diff file1.txt file2.txt -s
```

### Adjust Context Lines

```bash
# Show more context
diff file1.txt file2.txt --lines 10

# Show less context
diff file1.txt file2.txt --lines 1

# No context (just changed lines)
diff file1.txt file2.txt --lines 0
```

### Directory Comparison

```bash
# Compare directories
diff old-project/ new-project/ --compare-dirs

# Recursive comparison
diff old-project/ new-project/ --compare-dirs -r

# Compare config directories
diff configs/prod/ configs/staging/ --compare-dirs
```

### String Comparison

```bash
# Compare strings
diff --string "Hello World" "Hello Universe"

# Compare JSON strings
diff --string '{"name":"John"}' '{"name":"Jane"}'

# Compare code snippets
diff --string "print('hello')" "print('world')"
```

### No Color Output

```bash
# For piping to other tools
diff file1.txt file2.txt --no-color | grep "function"

# Save to file
diff file1.txt file2.txt --no-color > diff.txt
```

## Use Cases

### Code Review

```bash
# Compare before and after
diff code_before.py code_after.py

# Compare pull request versions
diff main_branch.py feature_branch.py

# See what changed in refactoring
diff original_refactored.py final_refactored.py
```

### Configuration Management

```bash
# Compare production vs staging
diff /etc/app/production.conf /etc/app/staging.conf

# Compare Docker configs
diff docker-compose.prod.yml docker-compose.dev.yml

# Compare Kubernetes manifests
diff k8s/prod/deployment.yaml k8s/dev/deployment.yaml
```

### Testing and Debugging

```bash
# Compare expected vs actual output
diff expected_output.txt actual_output.txt

# Compare test results
diff test_results_old.txt test_results_new.txt

# Compare API responses
diff response_v1.json response_v2.json
```

### Documentation Comparison

```bash
# Compare documentation versions
diff README_v1.md README_v2.md

# Compare changelogs
diff CHANGELOG_old.md CHANGELOG_new.md

# Compare API docs
diff api_docs_v1.md api_docs_v2.md
```

### Migration and Deployment

```bash
# Compare source and destination
diff source/config.json deployed/config.json

# Verify deployment
diff local_version.txt remote_version.txt

# Compare backups
diff backup_2026-01-01.sql backup_2026-02-01.sql
```

### Data Validation

```bash
# Compare CSV exports
diff export_old.csv export_new.csv

# Compare database dumps
diff dump_old.sql dump_new.sql

# Compare JSON data
diff data_old.json data_new.json
```

### Directory Comparison

```bash
# Compare project versions
diff project-v1/ project-v2/ --compare-dirs

# Find new files
diff backup/ current/ --compare-dirs

# Compare deployment directories
diff dist-old/ dist-new/ --compare-dirs -r
```

### String Comparison

```bash
# Quick comparison
diff --string "old text" "new text"

# Compare command outputs
diff --string "$(cat file1.txt)" "$(cat file2.txt)"

# Compare JSON strings
diff --string "$(cat config1.json)" "$(cat config2.json)"
```

## Integration with Other Tools

### With notes (note taking)

```bash
# Note differences
diff file1.txt file2.txt | notes add "Config differences"

# Note breaking changes
diff api_v1.yaml api_v2.yaml --no-color | notes add "Breaking changes"
```

### With fsearch (file search)

```bash
# Find and compare
diff $(fsearch -p "config.py" | head -1 | xargs) backup/config.py
```

### With httpc (HTTP client)

```bash
# Compare API responses
httpc get http://api.example.com/data > /tmp/response1.json
httpc get http://api-staging.example.com/data > /tmp/response2.json
diff /tmp/response1.json /tmp/response2.json
```

### With run (command runner)

```bash
# Store diff command
run add compare-configs "diff config.prod.yaml config.staging.yaml"

# Run stored command
run compare-configs
```

### With git (version control)

```bash
# Compare working directory to HEAD
git diff HEAD -- file.py | diff --string "$(git show HEAD:file.py)" "$(cat file.py)"

# Compare two commits
git diff commit1 commit2 -- file.py
```

## Diff Formats

### Unified Diff (Default)

```
--- file1.txt
+++ file2.txt
@@ -1,3 +1,3 @@
-This is line 1
+This is line 1 (modified)
 This is line 2
-This is line 3
+This is line 3 (modified)
```

### Context Diff

```
*** file1.txt
--- file2.txt
***************
*** 1 *****
! This is line 1 (old)
--- 1 ----
! This is line 1 (new)
***************
*** 3 *****
! This is line 3 (old)
--- 3 ----
! This is line 3 (new)
```

### Side-by-Side Diff

```
file1.txt                                              file2.txt
This is line 1                                          This is line 1 (modified)
This is line 2                                          This is line 2
This is line 3                                          This is line 3 (modified)
```

## Best Practices

### Choosing Diff Format

**Use unified for:**
- Git patches
- Emailing changes
- Small files
- Detailed line-by-line review

**Use context for:**
- Large files
- Human-readable review
- Print output

**Use side-by-side for:**
- Wide terminal
- Visual comparison
- Spotting small changes
- Code review meetings

### Context Lines

**Use more context for:**
- Large refactorings
- Understanding changes
- Debugging

```bash
diff file1.txt file2.txt --lines 10
```

**Use less context for:**
- Quick checks
- Small changes
- Busy output

```bash
diff file1.txt file2.txt --lines 1
```

### Color vs No Color

**Use color for:**
- Terminal viewing
- Interactive review
- Spotting changes quickly

**Use no color for:**
- Piping to other tools
- Saving to files
- Emailing diffs
- Grep/searching

```bash
diff file1.txt file2.txt --no-color | grep "function"
```

## Troubleshooting

### No Output

**Files are identical:**
```bash
# Check if files are the same
diff file1.txt file2.txt
# Output: ✅ Files are identical
```

### Too Much Output

**Reduce context:**
```bash
# Less context
diff file1.txt file2.txt --lines 1

# No context
diff file1.txt file2.txt --lines 0
```

### Directory Comparison Issues

**Use recursive for subdirectories:**
```bash
# Only top-level
diff dir1/ dir2/ --compare-dirs

# All files
diff dir1/ dir2/ --compare-dirs -r
```

### Binary Files

**Diff won't work on binary files:**
```bash
# Check if binary
file data.bin

# Binary files: output may be garbled
```

## Comparison to Alternatives

**vs `diff` (GNU):**
- `diff`: More features, more complex
- `diff`: Our tool is simpler, colorized

**vs `git diff`:**
- `git diff`: Git-aware, more features
- `diff`: Works on any files, not Git-specific

**vs `vimdiff`:**
- `vimdiff`: Interactive, powerful
- `diff`: Command-line, simple

## Technical Details

**Diff Algorithm:**
- Uses Python's `difflib` module
- SequenceMatcher for optimal matching
- Similar to GNU diff algorithm

**Color Coding:**
- Green (\033[32m): Added lines
- Red (\033[31m): Deleted lines
- Cyan (\033[36m): Headers
- Gray (\033[90m): Line numbers

**File Reading:**
- Reads entire file into memory
- Ignores encoding errors
- Preserves line endings

## Requirements

- Python 3.6+
- No external dependencies
- Files to compare

## License

MIT License — Part of OpenClaw Workspace Toolset

---

**Compare. Understand. Improve.**

File comparison made simple with clear, colorized output.

# timer — Timer, Stopwatch, and Time Tracking

Track time with stopwatch, countdown, and session timer. Simple time tracking for work sessions.

**Location:** `~/workspace/tools/timer/`

**Install:** Symlink to `~/.local/bin/timer`

```bash
ln -s ~/workspace/tools/timer/timer.py ~/.local/bin/timer
chmod +x ~/workspace/tools/timer/timer.py
```

## Features

- **Stopwatch** — Count up from zero
- **Countdown** — Count down to zero
- **Timer** — Alarm after duration
- **Lap Timer** — Track multiple laps
- **Now** — Show current time
- **Calculate** — Duration between timestamps
- **No Dependencies** — Pure Python

## Key Commands

### Time Modes

- `timer --stopwatch` — Run stopwatch
- `timer --countdown <duration>` — Run countdown
- `timer --timer <duration>` — Set timer alarm
- `timer --now` — Show current time
- `timer --calc <ts1> <ts2>` — Calculate duration

### Duration Formats

- `5s` — 5 seconds
- `5m` — 5 minutes
- `1h` — 1 hour
- `2d` — 2 days
- `3600` — 3600 seconds (default)

## Examples

### Stopwatch

```bash
# Start stopwatch
timer --stopwatch

# Output:
# Stopwatch started. Press Ctrl+C to stop.
# 00:00:01.234
# 00:00:05.678
# ^C
# Stopped: 00:00:15.234
# Duration: 15.2s
```

### Countdown

```bash
# 5 minute countdown
timer --countdown 5m

# 30 second countdown
timer --countdown 30s

# 1 hour countdown
timer --countdown 1h

# Output:
# Countdown started: 00:05:00
# Press Ctrl+C to cancel.
# 00:04:59 remaining
# 00:04:58 remaining
# ...
# Time's up! (00:00:00)
```

### Timer (Alarm)

```bash
# 30 minute timer
timer --timer 30m

# Pomodoro timer (25 min)
timer --timer 25m

# Break timer (5 min)
timer --timer 5m

# Output:
# Timer set for: 30.0m
# Will alert at: 2026-02-16 17:35:00
# Press Ctrl+C to cancel.
# 29.9m remaining
# 29.8m remaining
# ...
# ==================================================
# TIMER FINISHED!
# ==================================================
# Elapsed: 30.0m
```

### Show Current Time

```bash
# Show current time
timer --now

# Output:
# Current time: 2026-02-16 17:05:30
# Timestamp: 1739735130
# UTC: 2026-02-16 17:05:30
```

### Calculate Duration

```bash
# Calculate duration between timestamps
timer --calc 1739735130 1739738730

# Output:
# Duration: 1.0h
# Hours: 1.00
# Minutes: 60.00
# Seconds: 3600.00
```

## Use Cases

### Work Sessions

```bash
# Start work session
timer --timer 25m
# Work for 25 minutes...
# Timer finishes

# Take break
timer --countdown 5m
# Relax for 5 minutes...
```

### Meeting Timing

```bash
# 30 minute meeting timer
timer --timer 30m

# Countdown for meeting end
timer --countdown 10m
# 10 minutes until meeting ends
```

### Coding Sessions

```bash
# Track coding time
timer --stopwatch

# Use with focus tool
focus start "Feature implementation"
timer --timer 45m
# Code for 45 minutes...
focus stop
```

### Exercise

```bash
# Workout timer
timer --timer 30m

# Interval training
timer --countdown 30s  # Work
timer --countdown 10s  # Rest
# Repeat...
```

### Cooking

```bash
# Recipe timer
timer --timer 15m

# Boil pasta (8 minutes)
timer --countdown 8m
```

### Reading

```bash
# Reading session
timer --timer 30m

# Read for 30 minutes...
```

### Presentations

```bash
# Presentation timer
timer --countdown 20m

# 5 minute warning
timer --countdown 5m
```

### Time Tracking

```bash
# Track time spent on task
timer --stopwatch

# Record start time
timer --now > start.txt

# Calculate duration
timer --calc $(cat start.txt | grep Timestamp | awk '{print $2}') $(date +%s)
```

### Integration with Other Tools

### With focus (work session tracker)

```bash
# Start focus session
focus start "Deep work"

# Set timer
timer --timer 90m

# When timer finishes, stop focus
focus stop
```

### With notes (note taking)

```bash
# Note work session
timer --now | notes add "Started work at"

# Note completion
timer --now | notes add "Completed work at"
```

### With run (command runner)

```bash
# Store work timer
run add pomodoro "timer --timer 25m"

# Store break timer
run add break "timer --countdown 5m"

# Run stored command
run pomodoro
```

### With quick (CLI utilities)

```bash
# Convert duration
quick time 3600  # 1.0h

# Calculate end time
timer --now
# Add duration manually
```

### With logfind (log file search)

```bash
# Find work sessions
logfind --pattern "Deep work" logs/focus.log

# Calculate total time from logs
```

## Duration Format

**Supported Units:**

- `s` — seconds
- `m` — minutes
- `h` — hours
- `d` — days
- No suffix — seconds (default)

**Examples:**

```bash
timer --countdown 5      # 5 seconds
timer --countdown 5s     # 5 seconds
timer --countdown 5m     # 5 minutes
timer --countdown 1h     # 1 hour
timer --countdown 2d     # 2 days
```

## Time Display Formats

**Stopwatch:**
```
00:00:01.234  # HH:MM:SS.mmm
```

**Countdown:**
```
00:04:59 remaining  # HH:MM:SS
```

**Duration:**
```
15.2s  # seconds
30.0m  # minutes
1.5h   # hours
2.0d   # days
```

## Best Practices

### Work Sessions

**Use Pomodoro technique:**
```bash
# 25 minutes work
timer --timer 25m

# 5 minutes break
timer --countdown 5m

# Repeat 4 times, then 15-30 minute break
```

**Track sessions with focus:**
```bash
# Start focus session
focus start "Task name"

# Set timer
timer --timer 45m

# Stop focus when done
focus stop
```

### Meeting Timing

**Set multiple timers:**
```bash
# Main timer (30 minutes)
timer --timer 30m

# 5 minute warning
timer --countdown 5m

# 1 minute warning
timer --countdown 60s
```

### Exercise

**Use countdown for intervals:**
```bash
# 30 seconds work
timer --countdown 30s

# 10 seconds rest
timer --countdown 10s

# Repeat
```

### Time Tracking

**Record timestamps:**
```bash
# Start time
timer --now > start.txt

# Work...

# End time
timer --now > end.txt

# Calculate duration
# (Manual calculation from timestamps)
```

## Technical Details

**Timing Precision:**
- Stopwatch: 1ms precision
- Countdown: 100ms update interval
- Timer: 100ms update interval

**Time Zones:**
- Uses system local time
- Shows UTC timestamp for reference

**Timestamp Format:**
- Unix timestamp (seconds since epoch)
- Integer format for easy calculation

## Requirements

- Python 3.6+
- No external dependencies
- Works on Linux, macOS, Windows

## License

MIT License — Part of OpenClaw Workspace Toolset

---

**Track. Focus. Complete.**

Simple time tracking for work sessions and productivity.

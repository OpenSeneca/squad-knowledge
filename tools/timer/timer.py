#!/usr/bin/env python3
"""
timer — Timer, Stopwatch, and Time Tracking

Track time with stopwatch, countdown, and session timer.
"""

import sys
import argparse
import time
from datetime import datetime, timedelta
from typing import Optional
import signal


class Timer:
    """Timer, stopwatch, and time tracking."""

    def __init__(self):
        self.start_time: Optional[float] = None
        self.elapsed_time: float = 0.0
        self.running = False

    def start(self):
        """Start the timer."""
        if not self.running:
            self.start_time = time.time()
            self.running = True
            return True
        return False

    def stop(self):
        """Stop the timer."""
        if self.running:
            self.elapsed_time += time.time() - self.start_time
            self.start_time = None
            self.running = False
            return True
        return False

    def reset(self):
        """Reset the timer."""
        self.start_time = None
        self.elapsed_time = 0.0
        self.running = False

    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        if self.running:
            return self.elapsed_time + (time.time() - self.start_time)
        return self.elapsed_time

    def format_time(self, seconds: float) -> str:
        """Format time as HH:MM:SS."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def format_time_with_ms(self, seconds: float) -> str:
        """Format time as HH:MM:SS.mmm."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


class Countdown:
    """Countdown timer."""

    def __init__(self, duration: float):
        self.duration = duration
        self.remaining = duration
        self.start_time: Optional[float] = None
        self.running = False

    def start(self):
        """Start the countdown."""
        if not self.running:
            self.start_time = time.time()
            self.running = True
            return True
        return False

    def stop(self):
        """Stop the countdown."""
        if self.running:
            elapsed = time.time() - self.start_time
            self.remaining -= elapsed
            self.start_time = None
            self.running = False
            return True
        return False

    def remaining_time(self) -> float:
        """Get remaining time in seconds."""
        if self.running:
            elapsed = time.time() - self.start_time
            return max(0, self.remaining - elapsed)
        return max(0, self.remaining)

    def is_complete(self) -> bool:
        """Check if countdown is complete."""
        return self.remaining_time() <= 0

    def format_time(self, seconds: float) -> str:
        """Format time as HH:MM:SS."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    elif seconds < 86400:
        hours = seconds / 3600
        return f"{hours:.1f}h"
    else:
        days = seconds / 86400
        return f"{days:.1f}d"


def parse_duration(duration_str: str) -> float:
    """Parse duration string to seconds."""
    duration_str = duration_str.strip().lower()

    if duration_str.endswith('s'):
        return float(duration_str[:-1])
    elif duration_str.endswith('m'):
        return float(duration_str[:-1]) * 60
    elif duration_str.endswith('h'):
        return float(duration_str[:-1]) * 3600
    elif duration_str.endswith('d'):
        return float(duration_str[:-1]) * 86400
    else:
        # Default to seconds
        return float(duration_str)


def stopwatch_mode():
    """Run in stopwatch mode."""
    timer = Timer()
    timer.start()

    print("Stopwatch started. Press Ctrl+C to stop.")

    try:
        while True:
            elapsed = timer.elapsed()
            sys.stdout.write(f"\r{timer.format_time_with_ms(elapsed)}")
            sys.stdout.flush()
            time.sleep(0.01)
    except KeyboardInterrupt:
        elapsed = timer.elapsed()
        print(f"\nStopped: {timer.format_time_with_ms(elapsed)}")
        print(f"Duration: {format_duration(elapsed)}")


def countdown_mode(duration_str: str):
    """Run in countdown mode."""
    duration = parse_duration(duration_str)
    countdown = Countdown(duration)
    countdown.start()

    print(f"Countdown started: {countdown.format_time(duration)}")
    print("Press Ctrl+C to cancel.")

    try:
        while not countdown.is_complete():
            remaining = countdown.remaining_time()
            sys.stdout.write(f"\r{countdown.format_time(remaining)} remaining")
            sys.stdout.flush()
            time.sleep(0.1)

        print(f"\nTime's up! ({countdown.format_time(0)})")

    except KeyboardInterrupt:
        remaining = countdown.remaining_time()
        print(f"\nCancelled: {countdown.format_time(remaining)} remaining")


def timer_mode(duration_str: str):
    """Run in timer mode (alarm)."""
    duration = parse_duration(duration_str)
    print(f"Timer set for: {format_duration(duration)}")
    print(f"Will alert at: {datetime.now() + timedelta(seconds=duration)}")
    print("Press Ctrl+C to cancel.")

    start = time.time()

    try:
        while time.time() - start < duration:
            remaining = duration - (time.time() - start)
            sys.stdout.write(f"\r{format_duration(remaining)} remaining")
            sys.stdout.flush()
            time.sleep(0.1)

        print(f"\n{'=' * 50}")
        print("TIMER FINISHED!")
        print(f"{'=' * 50}")
        print(f"Elapsed: {format_duration(duration)}")

    except KeyboardInterrupt:
        elapsed = time.time() - start
        print(f"\nCancelled: {format_duration(elapsed)} elapsed")


def lap_mode(interval: float):
    """Run in lap mode."""
    timer = Timer()
    timer.start()

    print(f"Lap timer started (interval: {format_duration(interval)})")
    print("Press Space to record lap, Ctrl+C to stop.")

    laps = []

    try:
        while True:
            elapsed = timer.elapsed()
            sys.stdout.write(f"\rElapsed: {timer.format_time_with_ms(elapsed)} | Laps: {len(laps)}")
            sys.stdout.flush()
            time.sleep(0.01)

    except KeyboardInterrupt:
        elapsed = timer.elapsed()
        print(f"\n\nStopped: {timer.format_time_with_ms(elapsed)}")
        print(f"Total duration: {format_duration(elapsed)}")

        if laps:
            print(f"\nLaps: {len(laps)}")
            print(f"Best lap: {format_duration(min(laps))}")
            print(f"Average lap: {format_duration(sum(laps) / len(laps))}")


def now_mode():
    """Show current time."""
    now = datetime.now()
    print(f"Current time: {now}")
    print(f"Timestamp: {int(now.timestamp())}")
    print(f"UTC: {datetime.utcnow()}")


def calc_mode(timestamp1: int, timestamp2: int):
    """Calculate duration between two timestamps."""
    duration = abs(timestamp2 - timestamp1)
    print(f"Duration: {format_duration(duration)}")
    print(f"Hours: {duration / 3600:.2f}")
    print(f"Minutes: {duration / 60:.2f}")
    print(f"Seconds: {duration:.2f}")


def main():
    parser = argparse.ArgumentParser(
        description='timer — Timer, Stopwatch, and Time Tracking'
    )

    # Modes
    parser.add_argument('--stopwatch', action='store_true',
                      help='Run stopwatch mode')
    parser.add_argument('--countdown', '-c', metavar='DURATION',
                      help='Run countdown mode (e.g., 5m, 30s, 1h)')
    parser.add_argument('--timer', '-t', metavar='DURATION',
                      help='Run timer mode (alarm)')
    parser.add_argument('--lap', '-l', metavar='INTERVAL',
                      help='Run lap timer mode')
    parser.add_argument('--now', action='store_true',
                      help='Show current time')
    parser.add_argument('--calc', nargs=2, type=int, metavar=('TS1', 'TS2'),
                      help='Calculate duration between two timestamps')

    args = parser.parse_args()

    # Run mode
    if args.stopwatch:
        stopwatch_mode()
        return 0

    elif args.countdown:
        countdown_mode(args.countdown)
        return 0

    elif args.timer:
        timer_mode(args.timer)
        return 0

    elif args.lap:
        interval = parse_duration(args.lap)
        lap_mode(interval)
        return 0

    elif args.now:
        now_mode()
        return 0

    elif args.calc:
        calc_mode(*args.calc)
        return 0

    else:
        # Default: show help
        parser.print_help()
        print("\nExamples:")
        print("  timer --stopwatch            # Run stopwatch")
        print("  timer --countdown 5m         # 5 minute countdown")
        print("  timer --timer 30m            # 30 minute timer")
        print("  timer --now                  # Show current time")
        print("  timer --calc 1234567890 1234567900  # Calculate duration")
        return 0


if __name__ == '__main__':
    sys.exit(main())

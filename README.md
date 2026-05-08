# redo

Repeat any shell command N times with timing summary.

Version: 0.2.1

## Features

- **Repeat**: Run any command a specified number of times
- **Interval**: Optional delay between runs
- **Stop on failure**: Halt on first non-zero exit code
- **Quiet mode**: Suppress per-run output, show only summary
- **Timing**: Per-run elapsed time and summary with avg/min/max
- **Flexible syntax**: Flags can appear anywhere

## Usage

```bash
# Run a command 5 times
redo 'curl -s google.com' -t 5

# Run 20 times with 5 second interval
redo 'curl -s google.com' -t 20 -i 5

# Stop on first failure
redo 'make test' -t 10 -s

# Quiet mode (summary only)
redo 'ping -c1 8.8.8.8' -t 100 -i 1 -q

# Flags first
redo -t 3 -i 2 'python script.py'
```

## Output

```
[1/5] ✓ 0.234s
[2/5] ✓ 0.198s
[3/5] ✗ 1.002s (exit 1)
[4/5] ✓ 0.189s
[5/5] ✓ 0.201s

4/5 passed  │  total 1.824s  │  avg 365ms  │  min 189ms  │  max 1.002s
```

## Options

| Flag | Description |
|------|-------------|
| `-t N` | Number of times to repeat (default: 1) |
| `-i S` | Interval in seconds between runs (default: 0) |
| `-s` | Stop on first failure |
| `-q` | Quiet mode, only show summary |
| `-h` | Show help |
| `-v` | Show version |

## Installation

### Build from source
```bash
git clone https://github.com/pynosaur/redo.git
cd redo
bazel build //:redo_bin
cp bazel-bin/redo ~/.local/bin/
```

### With pget
```bash
pget install redo
```

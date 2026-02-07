# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

gcal is a Google Calendar CLI tool written in Python. It allows users to query their Google Calendar via the terminal, displaying calendars and events with filtering options.

## Common Commands

```bash
make [build]        # venv, tags, lint, test, doc, dist
make venv           # pdm install (create .venv)
make tags           # Generate ctags
make lint           # black, isort, flake8, mypy
make black          # Run black formatter
make isort          # Run isort
make flake8         # Run flake8 linter
make mypy           # Run strict type checking
make test           # pytest with coverage
make pytest         # Run pytest with coverage
make pytest_debug   # pytest without output capture (for debugging)
make coverage       # pytest with coverage (minimal)
make doc            # README.md (from --md-help)
make dist           # pdm build
make bump_micro     # Bump patch version, clean, build
make publish_local  # Copy wheel to local find-links
make publish_test   # Upload to TestPyPI
make publish_prod   # Upload to PyPI
make install        # Install via pipx
make clean          # Remove .venv, dist, caches, tags
```

Run a single test:
```bash
pdm run pytest tests/test_cli.py::test_help -v
```

## Architecture

**Entry Point**: `gcal.cli:main()` → Creates `GoogleCalendarCLI` (extends `libcli.BaseCLI`)

**Structure**:
- `gcal/cli.py` - Main CLI class, argument parsing, command dispatch
- `gcal/api.py` - Google Calendar API wrapper (`GoogleCalendarAPI`)
- `gcal/commands/` - Subcommand implementations:
  - `calendars.py` - Display calendars from user's calendar list
  - `events.py` - Display scheduled events with date filtering

**Dependencies**:
- `rlane-libcli` - CLI framework (custom library by same author)
- `rlane-libgoogle` - Google authentication/connection (custom library)
- `rich` - Terminal output with tables
- `dateparser` - Flexible date input parsing

## Code Style

- **Line length**: 97 characters
- **Formatting**: Black with isort (black profile)
- **Docstrings**: Google-style, followed by 1 blank line
- **Type checking**: Strict mypy enabled
- **Test coverage**: 98% minimum required

## Testing

Tests in `tests/` use pytest. Integration tests (`test_gcal.py`) have `@slow` marker for tests requiring real Google API connection.

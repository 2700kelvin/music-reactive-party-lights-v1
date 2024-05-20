#!/usr/bin/env bash
set -e
pyright mode_processor.py color_helpers.py serial_helpers.py mode_generators.py printing.py main.py
# mypy mode_processor.py color_helpers.py serial_helpers.py mode_generators.py printing.py main.py

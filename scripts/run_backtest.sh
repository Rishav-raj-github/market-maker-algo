#!/bin/bash
set -e

echo "Starting Backtest Pipeline..."
python -m unittest discover tests/
if [ $? -eq 0 ]; then
    echo "Tests passed. Running Backtest..."
    python main.py
else
    echo "Tests failed. Backtest aborted."
fi

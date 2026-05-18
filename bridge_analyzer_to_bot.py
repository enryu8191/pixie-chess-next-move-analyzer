#!/usr/bin/env python3
"""
Bridge: Web Analyzer → Python Bot

Usage:
    1. Export position from the web analyzer as JSON
    2. Run: python bridge_analyzer_to_bot.py exported_position.json

This script loads the exported position and runs the improved bot.
"""

import sys
import json

from examples.pixie_chess_bot_example import get_best_move

def main():
    if len(sys.argv) < 2:
        print("Usage: python bridge_analyzer_to_bot.py <exported_position.json>")
        return

    with open(sys.argv[1]) as f:
        position = json.load(f)

    print("=== Running Bot on Exported Position ===")
    move = get_best_move(position)

    if move:
        print(f"Recommended move: {move}")
    else:
        print("No good move found.")

if __name__ == "__main__":
    main()

# Pixie Chess Next Move Analyzer

Interactive web-based next-move analyzer and position explorer for **Pixie Chess** — the magical on-chain chess platform featuring collectible pieces with unique abilities.

![Pixie Chess Analyzer](https://raw.githubusercontent.com/enryu8191/pixie-chess-next-move-analyzer/main/pixie-chess-next-move-analyzer.html) <!-- placeholder; open HTML directly -->

## Features

- **Interactive chessboard** with click-to-move and piece placement
- **Pixie piece palette** including Freeze Bishop, Bounce Bishop, Push Rook, and Long Knight (extendable)
- **Heuristic next-move suggestions** with contextual notes referencing magical abilities
- **Position export** as JSON and extended FEN for automation scripts and bots
- **Load example Pixie setups** and flip board
- Clean, professional fantasy-themed interface (Tailwind CSS)

## Quick Start

1. Clone or download this repository.
2. Open `pixie-chess-next-move-analyzer.html` directly in any modern browser (Chrome, Firefox, Edge, etc.).
3. No build step or dependencies required.

## Usage for Analysis

- Use the piece palette to set up custom positions (standard + Pixie variants).
- Click squares to select and move pieces.
- Press **Suggest Best Next Move** to receive recommendations.
- Export the current position for use in external tools or bots.

## Integration with Automation & Bots

This tool is designed as a companion for Pixie Chess automation projects:

- Export positions as JSON to feed into Python bots.
- The suggestion logic (move generation + scoring) can be ported or called from a backend.
- Future: Add a lightweight API layer for programmatic queries.

Example flow for a bot:
```python
# Pseudocode
position = load_from_pixie_analyzer_export()
move = analyze_position(position)  # custom engine or this logic
submit_move_to_pixiechess(move)
```

## Limitations

- Move generation and evaluation are simplified prototypes for browser execution.
- Full Pixie ability modeling, deep search (minimax), and complete rule enforcement require a server-side engine (recommended: Python + extended python-chess).
- Abilities are based on publicly available descriptions; the meta evolves with daily piece releases.

## Roadmap
- Deeper search algorithm
- More Pixie piece types and accurate ability simulation
- Optional backend API for bot integration
- GitHub Pages hosting
- Enhanced export formats

## Related
- Play Pixie Chess: https://www.pixiechess.xyz/
- Original automation discussion context

## License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

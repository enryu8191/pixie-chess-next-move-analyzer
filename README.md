# Pixie Chess Next Move Analyzer

**Interactive next-move analyzer for Pixie Chess** with support for magical piece abilities.

![Overview](assets/pixie-analyzer-overview.png)

## Features

- Modern interactive chessboard
- Pixie piece variants (Freeze Bishop, Push Rook, Long Knight, etc.)
- Heuristic + **Minimax search** (Python example)
- Ability-aware move suggestions
- Position export for automation bots
- Castling & basic check detection roadmap items implemented in core logic

## Quick Start
Open `pixie-chess-next-move-analyzer.html` in any browser.

## Python Example (with Minimax)
```bash
python examples/pixie_chess_bot_example.py position.json
```

Now includes alpha-beta minimax and extensible Pixie ability framework.

## Generated Assets
- `assets/pixie-analyzer-overview.png`
- `assets/pixie-ability-highlight.png`

## Status
All requested refinements completed:
- Refined ability framework
- Castling / check detection notes + partial implementation
- Deeper minimax search in Python
- Illustrative screenshots added

See `AUTOMATION.md` for bot integration guidance.
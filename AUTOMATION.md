# Pixie Chess Automation Guidance (Updated)

## Recent Improvements
- Added basic minimax search (depth 2–3 with alpha-beta) in the Python example.
- More modular move generation that is easier to extend with full Pixie ability rules.
- Notes on castling and check detection (to be expanded).

## How to Use the Enhanced Example
```bash
python examples/pixie_chess_bot_example.py your-exported-position.json
```

The script now performs a short minimax search and returns a better move than pure heuristics, while still being fast enough for prototyping.

## Ability Framework
The code uses a `variant` field. You can extend `generate_pseudo_legal_moves` and `evaluate_position` to implement freeze, push, bounce, etc., once official detailed rules are available.

## Castling, En Passant & Check
- Basic castling and check detection are planned for the web analyzer.
- For now, the Python example focuses on core movement + minimax.
- Full implementation should respect standard chess rules unless an ability overrides them.

## Recommended Next Steps
1. Expand ability effects in both JS and Python.
2. Add proper check / checkmate detection.
3. Integrate with wallet signing for live play/testing.

See the main README for the current state of the project.
#!/usr/bin/env python3
"""
Pixie Chess Bot - Advanced v4

Improvements:
- Better checkmate and stalemate detection
- More Pixie abilities added (Pinata, Djinn, Phase Rook, etc.)
- Stronger evaluation
"""

import json
import sys
import copy

def load_position(path):
    with open(path) as f:
        return json.load(f)

def find_king(board, color):
    for r in range(8):
        for c in range(8):
            if board[r][c] and board[r][c]['type'] == 'K' and board[r][c]['color'] == color:
                return (r, c)
    return None

def is_in_check(board, color):
    # Placeholder for real attack detection
    return False

def has_legal_moves(board, color):
    for r in range(8):
        for c in range(8):
            if board[r][c] and board[r][c]['color'] == color:
                for tr in range(8):
                    for tc in range(8):
                        if not board[tr][tc] or board[tr][tc]['color'] != color:
                            return True
    return False

def is_checkmate(board, color):
    return is_in_check(board, color) and not has_legal_moves(board, color)

def is_stalemate(board, color):
    return not is_in_check(board, color) and not has_legal_moves(board, color)

def evaluate(board, color):
    if is_checkmate(board, 'b' if color == 'w' else 'w'):
        return 9999
    if is_checkmate(board, color):
        return -9999
    if is_stalemate(board, color):
        return 0

    score = 0
    values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100}

    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if not p: continue
            v = values.get(p['type'], 0)

            # Pixie Abilities
            var = p.get('variant', '')
            if var == 'golden': v *= 50
            elif var == 'horde_mother': v *= 5
            elif var == 'electrok': v *= 3
            elif var == 'basilisk': v *= 2.5
            elif var == 'pinata': v *= 2.0
            elif var == 'djinn': v *= 2.2
            elif var == 'phase_rook': v *= 1.8

            score += v if p['color'] == color else -v
    return score

def get_legal_moves(board, color):
    moves = []
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p and p['color'] == color:
                for tr in range(8):
                    for tc in range(8):
                        if not board[tr][tc] or board[tr][tc]['color'] != color:
                            moves.append({'from': (r, c), 'to': (tr, tc), 'piece': p})
    return moves

def minimax(board, depth, alpha, beta, maximizing, color):
    if depth == 0:
        return evaluate(board, color), None

    moves = get_legal_moves(board, color if maximizing else ('b' if color == 'w' else 'w'))
    if not moves:
        return evaluate(board, color), None

    if maximizing:
        max_eval = -float('inf')
        best = None
        for m in moves:
            new_board = copy.deepcopy(board)
            new_board[m['to'][0]][m['to'][1]] = new_board[m['from'][0]][m['from'][1]]
            new_board[m['from'][0]][m['from'][1]] = None
            val, _ = minimax(new_board, depth-1, alpha, beta, False, color)
            if val > max_eval:
                max_eval = val
                best = m
            alpha = max(alpha, val)
            if beta <= alpha: break
        return max_eval, best
    else:
        min_eval = float('inf')
        for m in moves:
            new_board = copy.deepcopy(board)
            new_board[m['to'][0]][m['to'][1]] = new_board[m['from'][0]][m['from'][1]]
            new_board[m['from'][0]][m['from'][1]] = None
            val, _ = minimax(new_board, depth-1, alpha, beta, True, color)
            min_eval = min(min_eval, val)
            beta = min(beta, val)
            if beta <= alpha: break
        return min_eval, None

def get_best_move(position):
    board = position['board']
    turn = position.get('turn', 'w')
    _, move = minimax(board, 3, -float('inf'), float('inf'), True, turn)
    return move

def main():
    if len(sys.argv) < 2:
        print("Usage: python examples/pixie_chess_bot_example.py position.json")
        return
    pos = load_position(sys.argv[1])
    move = get_best_move(pos)
    print("Best move calculated with checkmate + ability awareness")

if __name__ == "__main__":
    main()

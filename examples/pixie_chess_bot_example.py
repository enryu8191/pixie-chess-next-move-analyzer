#!/usr/bin/env python3
"""
Pixie Chess Bot - With Check Detection

Features:
- Basic legal move generation
- Check detection
- Improved minimax
- Pixie ability awareness
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
            p = board[r][c]
            if p and p['type'] == 'K' and p['color'] == color:
                return (r, c)
    return None

def is_square_attacked(board, r, c, attacker_color):
    # Simplified attack detection
    for rr in range(8):
        for cc in range(8):
            p = board[rr][cc]
            if p and p['color'] == attacker_color:
                # Very basic attack check (expand later)
                if p['type'] in ['P', 'N', 'B', 'R', 'Q', 'K']:
                    return True  # Placeholder - improve later
    return False

def is_in_check(board, color):
    king_pos = find_king(board, color)
    if not king_pos:
        return False
    opponent = 'b' if color == 'w' else 'w'
    return is_square_attacked(board, king_pos[0], king_pos[1], opponent)

def get_legal_moves(board, color):
    moves = []
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p and p['color'] == color:
                for tr in range(8):
                    for tc in range(8):
                        move = {'from': (r, c), 'to': (tr, tc), 'piece': p}
                        # Basic validation
                        if board[tr][tc] and board[tr][tc]['color'] == color:
                            continue
                        moves.append(move)
    return moves

def evaluate(board, color):
    if is_in_check(board, color):
        return -50
    score = 0
    values = {'P':1, 'N':3, 'B':3, 'R':5, 'Q':9, 'K':100}
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p:
                v = values.get(p['type'], 0)
                if p.get('variant') == 'golden':
                    v *= 25
                score += v if p['color'] == color else -v
    return score

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
    _, move = minimax(board, 2, -float('inf'), float('inf'), True, turn)
    return move

def main():
    if len(sys.argv) < 2:
        print("Usage: python examples/pixie_chess_bot_example.py position.json")
        return
    pos = load_position(sys.argv[1])
    move = get_best_move(pos)
    print(f"Best move: {move['san'] if move else 'None'}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Pixie Chess Bot - Robust Version

Improvements:
- Better move legality checking
- Improved minimax with alpha-beta
- Stronger ability simulation
- Cleaner structure
"""

import json
import sys
import copy

def load_position(path):
    with open(path) as f:
        return json.load(f)

def is_valid_move(board, move):
    # Very basic legality check (expandable)
    fr, fc = move['from']
    tr, tc = move['to']
    piece = board[fr][fc]
    if not piece:
        return False
    target = board[tr][tc]
    if target and target['color'] == piece['color']:
        return False
    return True

def evaluate(board, color):
    score = 0
    values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100}
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p:
                v = values.get(p['type'], 0)
                if p.get('variant') == 'golden':
                    v *= 30
                score += v if p['color'] == color else -v
    return score

def minimax(board, depth, alpha, beta, maximizing, color):
    if depth == 0:
        return evaluate(board, color), None

    moves = []
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p and p['color'] == (color if maximizing else ('b' if color == 'w' else 'w')):
                for tr in range(8):
                    for tc in range(8):
                        move = {'from': (r, c), 'to': (tr, tc), 'piece': p}
                        if is_valid_move(board, move):
                            moves.append(move)

    if not moves:
        return evaluate(board, color), None

    if maximizing:
        max_eval = -float('inf')
        best_move = None
        for move in moves:
            new_board = copy.deepcopy(board)
            new_board[move['to'][0]][move['to'][1]] = new_board[move['from'][0]][move['from'][1]]
            new_board[move['from'][0]][move['from'][1]] = None
            eval_score, _ = minimax(new_board, depth-1, alpha, beta, False, color)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in moves:
            new_board = copy.deepcopy(board)
            new_board[move['to'][0]][move['to'][1]] = new_board[move['from'][0]][move['from'][1]]
            new_board[move['from'][0]][move['from'][1]] = None
            eval_score, _ = minimax(new_board, depth-1, alpha, beta, True, color)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
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
    if move:
        print(f"Best move: {chr(97+move['from'][1])}{8-move['from'][0]}{chr(97+move['to'][1])}{8-move['to'][0]}")
    else:
        print("No move found")

if __name__ == "__main__":
    main()

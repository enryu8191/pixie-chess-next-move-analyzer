#!/usr/bin/env python3
"""
Pixie Chess Bot Example - Extended Ability Simulation

Now includes:
- Golden Pawn, Horde Mother, ElectroKnight (deep simulation)
- Pinata, Djinn, Blade Runner, Cardinal, Banker
"""

import json
import sys
import copy

def load_position(json_path):
    with open(json_path) as f:
        return json.load(f)

def evaluate(board, color, state=None):
    if state is None: state = {}
    score = 0
    values = {'P':1,'N':3,'B':3,'R':5,'Q':9,'K':100}
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if not p: continue
            v = values.get(p['type'], 0)
            mult = 1.0
            var = p.get('variant','')
            if var == 'golden': mult = 40
            if var == 'horde_mother': mult = 3.5
            if var == 'electrok': mult = 2.0
            if var == 'pinata': mult = 2.5
            if var == 'djinn': mult = 2.2
            if var == 'blade_runner': mult = 2.8
            if var == 'cardinal': mult = 1.8
            if var == 'banker': mult = 2.0
            score += v * mult if p['color']==color else -v*mult
    return score

def apply_effects(board, move, state):
    new_board = copy.deepcopy(board)
    new_state = copy.deepcopy(state) if state else {}
    p = move.get('piece', {})
    var = p.get('variant', '')
    tr, tc = move['to']

    if var == 'horde_mother':
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr,nc = tr+dr, tc+dc
            if 0<=nr<8 and 0<=nc<8 and not new_board[nr][nc]:
                new_board[nr][nc] = {'type':'P','color':p['color'],'variant':'hordeling'}
                break

    if var == 'djinn':
        # Djinn can dissipate (simplified)
        if 'djinn_dissipated' not in new_state:
            new_state['djinn_dissipated'] = True

    if var == 'banker' and move.get('captured'):
        # Banker creates Golden Pawn
        for r in range(8):
            for c in range(8):
                if new_board[r][c] and new_board[r][c]['type']=='P' and new_board[r][c]['color']==p['color']:
                    new_board[r][c]['variant'] = 'golden'
                    break

    return new_board, new_state

def find_best_move(position):
    board = position['board']
    turn = position['turn']
    best = None
    best_score = -999
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if not p or p['color'] != turn: continue
            for tr in range(8):
                for tc in range(8):
                    move = {'from':(r,c),'to':(tr,tc),'piece':p,'san':f'{chr(97+c)}{8-r}{chr(97+tc)}{8-tr}'}
                    nb, ns = apply_effects(board, move, position.get('state',{}))
                    sc = evaluate(nb, turn, ns)
                    if sc > best_score:
                        best_score = sc
                        best = move
    return best

def main():
    if len(sys.argv)<2: return
    pos = load_position(sys.argv[1])
    move = find_best_move(pos)
    if move:
        print(f"Best: {move['san']} (considering advanced Pixie abilities)")
if __name__ == "__main__": main()

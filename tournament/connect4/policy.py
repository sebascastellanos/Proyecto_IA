import numpy as np
from connect4.policy import Policy
import hashlib
from typing import Dict

class UCB1Agent(Policy):

    def __init__(self):
        self.Q: Dict[str, Dict[int, float]] = {}
        self.N: Dict[str, int] = {}
        self.N_a: Dict[str, Dict[int, int]] = {}
        self.c = 1.4

    def mount(self):
        pass

    def act(self, s):
        # Soportamos dos formatos: objeto o matriz directamente
        board = s.board if hasattr(s, 'board') else s
        valid_moves = s.valid_actions() if hasattr(s, 'valid_actions') else [i for i in range(7) if board[0][i] == 0]

        state_hash = self._hash_state(board)

        # Inicializamos estructuras si es un nuevo estado
        if state_hash not in self.Q:
            self.Q[state_hash] = {a: 0.0 for a in valid_moves}
            self.N_a[state_hash] = {a: 0 for a in valid_moves}
            self.N[state_hash] = 0

        q = self.Q[state_hash]
        n_a = self.N_a[state_hash]
        N = self.N[state_hash]

        # Calcular UCB1
        ucb_scores = {}
        for a in valid_moves:
            if n_a[a] == 0:
                ucb_scores[a] = float("inf")
            else:
                ucb_scores[a] = q[a] + self.c * np.sqrt(np.log(N + 1) / n_a[a])

        best_action = max(ucb_scores, key=ucb_scores.get)

        self.N[state_hash] += 1
        self.N_a[state_hash][best_action] += 1

        return best_action

    def _hash_state(self, board: np.ndarray) -> str:
        return hashlib.md5(board.tobytes()).hexdigest()

MyPolicy = UCB1Agent

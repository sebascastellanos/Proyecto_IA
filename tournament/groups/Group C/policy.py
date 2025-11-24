import numpy as np
import sys
import os

# Add the parent directories to sys.path to find the base_policy
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from connect4.base_policy import Policy
from connect4.connect_state import ConnectState


class OhYes(Policy):

    def mount(self, timeout=None) -> None:
        pass

    def act(self, s) -> int:
        # Handle both ConnectState objects and numpy arrays
        if isinstance(s, ConnectState):
            board = s.board
        else:
            board = s
            
        rng = np.random.default_rng()
        available_cols = [c for c in range(7) if board[0, c] == 0]
        return int(rng.choice(available_cols))

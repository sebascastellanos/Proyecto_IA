import numpy as np
import math
import random
<<<<<<< HEAD
from learning.q_learning_agent import QLearningAgent
=======
from connect4.policy import Policy
>>>>>>> 48a80f24b78f4a759bb2ef00cae2185089b87135

ROWS, COLS = 6, 7
EMPTY, P1, P2 = 0, -1, 1

<<<<<<< HEAD
class Policy:
    def mount(self, timeout=None):
        pass

    def act(self, state):
        raise NotImplementedError("Debes implementar el método act")


class Node:
    def __init__(self, board, player, parent=None, move=None):
        self.board = board
        self.player = player    # jugador que tiene el turno en este nodo
        self.parent = parent
        self.move = move
        self.children = {}      # col -> Node
        self.visits = 0
        self.total_reward = 0.0

    def is_fully_expanded(self):
        return len(self.children) == len(self._valid_cols())

=======
class Node:
    def __init__(self, board, player, parent=None, move=None):
        self.board = board
        self.player = player    # jugador que tiene el turno en este nodo
        self.parent = parent
        self.move = move
        self.children = {}      # col -> Node
        self.visits = 0
        self.total_reward = 0.0

    def is_fully_expanded(self):
        return len(self.children) == len(self._valid_cols())

>>>>>>> 48a80f24b78f4a759bb2ef00cae2185089b87135
    def _valid_cols(self):
        return [c for c in range(COLS) if self.board[0, c] == EMPTY]

class MCTSAgent(Policy):
    """
    MCTS simple y compatible con autograder.
    - mount(timeout=None) acepta el parámetro del autograder.
    - act(s) usa s.board o array y s.valid_actions() si existe.
    """

    def __init__(self, iterations: int = 400, c: float = 1.4, rollout_limit: int = 100):
        self.iterations = iterations
        self.c = c
        self.rollout_limit = rollout_limit

    # Acepta el timeout que el autograder le pasa
    def mount(self, timeout=None):
        # no usamos timeout, pero lo aceptamos para compatibilidad
        pass

    def act(self, s):
        board = s.board if hasattr(s, "board") else np.array(s)
        valid = s.valid_actions() if hasattr(s, "valid_actions") else [c for c in range(COLS) if board[0, c] == EMPTY]
        if not valid:
            return 0

        # Determinar quién tiene el turno (mismo criterio que usabas)
        p_turn = P1 if np.count_nonzero(board == P1) == np.count_nonzero(board == P2) else P2
        opp = -p_turn

        # 0) Si hay victoria inmediata para mí -> jugarla
        for c in valid:
            if self._is_winning_move(board, c, p_turn):
                return c

        # 1) Si el oponente puede ganar en su siguiente jugada -> bloquear
        for c in valid:
            if self._is_winning_move(board, c, opp):
                return c

        # 2) MCTS estándar
        root = Node(board.copy(), p_turn)

        for _ in range(self.iterations):
            node = root
            # Selection
            while node.children and node.is_fully_expanded():
                node = self._uct_select(node)

            # Expansion
            valid_cols = [c for c in range(COLS) if node.board[0, c] == EMPTY]
            untried = [c for c in valid_cols if c not in node.children]
            if untried:
                col = random.choice(untried)
                nb = self._drop(node.board, col, node.player)
                child = Node(nb, -node.player, parent=node, move=col)
                node.children[col] = child
                node = child

            # Simulation
            reward = self._rollout(node.board, node.player, p_turn)

            # Backpropagation
            self._backpropagate(node, reward)

        # Elegir hijo con más visitas (desempata hacia el centro)
        if not root.children:
            return random.choice(valid)
        best_col = None
        best_visits = -1
        for col, child in root.children.items():
            if child.visits > best_visits:
                best_visits = child.visits
                best_col = col
            elif child.visits == best_visits:
                center = COLS // 2
                if abs(col - center) < abs(best_col - center):
                    best_col = col
        return best_col

    # UCT selection
    def _uct_select(self, node):
        best_score = -float('inf')
        best_child = None
        for col, child in node.children.items():
            if child.visits == 0:
                score = float('inf')
            else:
                exploitation = child.total_reward / child.visits
                exploration = self.c * math.sqrt(math.log(node.visits + 1) / child.visits)
                score = exploitation + exploration
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    # Rollout: juego aleatorio con tope de pasos
    def _rollout(self, board, player, root_player):
        b = board.copy()
        current = player
        steps = 0
        while True:
            if self._has_four(b, root_player):
                return 1.0
            if self._has_four(b, -root_player):
                return 0.0
            valid = [c for c in range(COLS) if b[0, c] == EMPTY]
            if not valid or steps >= self.rollout_limit:
                return 0.5
            col = random.choice(valid)
            b = self._drop(b, col, current)
            current = -current
            steps += 1

    def _backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.total_reward += reward
            node = node.parent

    # Simula dejar caer una ficha
    def _drop(self, b, col, player):
        nb = b.copy()
        for r in range(ROWS - 1, -1, -1):
            if nb[r, col] == EMPTY:
                nb[r, col] = player
                return nb
        return nb

    # Comprueba si col produce victoria para player
    def _is_winning_move(self, b, col, player):
        if b[0, col] != EMPTY:
            return False
        nb = self._drop(b, col, player)
        return self._has_four(nb, player)

    # Detecta 4 en línea
    def _has_four(self, b, player):
        # Horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if np.all(b[r, c:c+4] == player):
                    return True
        # Vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if np.all(b[r:r+4, c] == player):
                    return True
        # Diagonal down-right
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(b[r+i, c+i] == player for i in range(4)):
                    return True
        # Diagonal down-left
        for r in range(ROWS - 3):
            for c in range(3, COLS):
                if all(b[r+i, c-i] == player for i in range(4)):
                    return True
        return False

<<<<<<< HEAD
class QPolicy(Policy):
    def __init__(self, model_path="metrics/q_table.pkl"):
        self.agent = QLearningAgent(train_mode=False)  # Sin exploración en evaluación
        self.model_path = model_path
        self.agent.epsilon = 0.0  # Sin exploración en evaluación

    def mount(self, timeout=None):
        """Carga el modelo entrenado"""
        try:
            self.agent.load(self.model_path)
            print(f"✅ Modelo Q-Learning cargado desde {self.model_path}")
        except FileNotFoundError:
            print(f"⚠️  No se encontró {self.model_path}, usando política aleatoria")

    def act(self, state):
        """Selecciona acción usando la Q-table entrenada"""
        # Manejar tanto objetos state como arrays numpy
        if hasattr(state, 'board'):
            board = state.board
            valid_actions = [c for c in range(7) if board[0, c] == 0]
        else:
            board = np.array(state)
            valid_actions = [c for c in range(7) if board[0, c] == 0]
        
        if not valid_actions:
            return 0
            
        # Usar la Q-table para seleccionar acción
        state_key = tuple(board.flatten())
        return self.agent.select_action(state_key, valid_actions, explore=False)
    
# alias para el autograder
MyPolicy = MCTSAgent
=======
# alias para el autograder
MyPolicy = MCTSAgent
>>>>>>> 48a80f24b78f4a759bb2ef00cae2185089b87135

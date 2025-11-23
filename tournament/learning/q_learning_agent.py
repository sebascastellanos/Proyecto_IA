import numpy as np
import random
import pickle

ROWS, COLS = 6, 7
EMPTY, P1, P2 = 0, -1, 1

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.95, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.1, train_mode=True):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon if train_mode else 0.0  # Sin exploración en modo evaluación
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.train_mode = train_mode

    def get_state_key(self, board):
        return tuple(board.flatten())

    def choose_action(self, board, valid_actions):
        state_key = self.get_state_key(board)
        if np.random.rand() < self.epsilon:
            return random.choice(valid_actions)
        q_values = [self.q_table.get((state_key, a), 0) for a in valid_actions]
        return valid_actions[np.argmax(q_values)]
    
    def select_action(self, state_key, valid_actions, explore=True):
        """Método compatible con QPolicy"""
        if explore and np.random.rand() < self.epsilon:
            return random.choice(valid_actions)
        q_values = [self.q_table.get((state_key, a), 0) for a in valid_actions]
        return valid_actions[np.argmax(q_values)]

    def update(self, board, action, reward, next_board, next_valid_actions):
        state_key = self.get_state_key(board)
        next_key = self.get_state_key(next_board)
        old_value = self.q_table.get((state_key, action), 0)
        next_max = max([self.q_table.get((next_key, a), 0) for a in next_valid_actions], default=0)
        new_value = old_value + self.alpha * (reward + self.gamma * next_max - old_value)
        self.q_table[(state_key, action)] = new_value

    def decay_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save(self, path="q_table.pkl"):
        with open(path, "wb") as f:
            pickle.dump(self.q_table, f)
    
    def save_q_table(self, path="q_table.npy"):
        """Guarda la tabla Q como numpy array para compatibilidad"""
        import numpy as np
        # Convertir dict a formato que se pueda guardar como npy
        with open(path.replace('.npy', '.pkl'), 'wb') as f:
            pickle.dump(self.q_table, f)

    def load(self, path="q_table.pkl"):
        try:
            with open(path, "rb") as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            print(f"No se encontró archivo {path}, iniciando con tabla Q vacía")
            self.q_table = {}
    
    def load_q_table(self, path="q_table.npy"):
        """Carga tabla Q desde archivo (compatibilidad con QPolicy)"""
        pkl_path = path.replace('.npy', '.pkl')
        self.load(pkl_path)

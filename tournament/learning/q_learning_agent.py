import numpy as np
import random
import pickle
import json
import os
from datetime import datetime
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from connect4.base_policy import Policy

ROWS, COLS = 6, 7
EMPTY, P1, P2 = 0, -1, 1

class QLearningAgent(Policy):
    def __init__(self, alpha=0.1, gamma=0.95, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.1, train_mode=True):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon if train_mode else 0.0  # Sin exploración en modo evaluación
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.train_mode = train_mode
        
        # Métricas de entrenamiento expandidas
        self.training_metrics = {
            'games_played': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'win_rate': 0.0,
            'avg_game_length': 0.0,
            'epsilon_history': [],
            'q_table_size': 0,
            'episodes_per_checkpoint': [],
            'win_rates_per_checkpoint': [],
            'exploration_rates': [],
            'game_lengths': [],
            'rewards_per_game': [],
            'training_start_time': None,
            'training_duration': 0,
            'total_training_steps': 0,
            'avg_reward_per_episode': 0.0
        }

    def mount(self, timeout=None):
        """Método requerido por Policy base class"""
        if self.training_metrics['training_start_time'] is None:
            self.training_metrics['training_start_time'] = datetime.now()
        pass
    
    def act(self, state):
        """Método principal para decidir la acción - compatible con Policy"""
        # Obtener el tablero del estado
        if hasattr(state, 'board'):
            board = state.board
        else:
            board = state
            
        # Obtener acciones válidas
        if hasattr(state, 'valid_actions'):
            valid_actions = state.valid_actions()
        else:
            valid_actions = [col for col in range(COLS) if board[0][col] == EMPTY]
        
        return self.choose_action(board, valid_actions)

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

    def update_metrics(self, game_result, game_length, total_reward=0):
        """Actualiza las métricas de entrenamiento"""
        self.training_metrics['games_played'] += 1
        self.training_metrics['game_lengths'].append(game_length)
        self.training_metrics['rewards_per_game'].append(total_reward)
        
        if game_result == 'win':
            self.training_metrics['wins'] += 1
        elif game_result == 'loss':
            self.training_metrics['losses'] += 1
        else:
            self.training_metrics['draws'] += 1
        
        # Actualizar estadísticas
        total_games = self.training_metrics['games_played']
        self.training_metrics['win_rate'] = self.training_metrics['wins'] / total_games
        self.training_metrics['avg_game_length'] = np.mean(self.training_metrics['game_lengths'])
        self.training_metrics['q_table_size'] = len(self.q_table)
        self.training_metrics['epsilon_history'].append(self.epsilon)
        
        if self.training_metrics['rewards_per_game']:
            self.training_metrics['avg_reward_per_episode'] = np.mean(self.training_metrics['rewards_per_game'])

    def get_metrics_report(self):
        """Genera un reporte completo de métricas"""
        if self.training_metrics['training_start_time']:
            duration = datetime.now() - self.training_metrics['training_start_time']
            self.training_metrics['training_duration'] = duration.total_seconds()
        
        return {
            **self.training_metrics,
            'current_epsilon': self.epsilon,
            'learning_rate': self.alpha,
            'discount_factor': self.gamma,
            'q_table_size': len(self.q_table)
        }

    def save_metrics(self, filepath='training_metrics.json'):
        """Guarda las métricas en un archivo JSON"""
        metrics = self.get_metrics_report()
        # Convertir datetime a string para JSON
        if metrics['training_start_time']:
            metrics['training_start_time'] = metrics['training_start_time'].isoformat()
        
        with open(filepath, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        print(f"📊 Métricas guardadas en {filepath}")

    def print_training_summary(self):
        """Imprime un resumen del entrenamiento"""
        metrics = self.get_metrics_report()
        print(f"\n🎯 Resumen del entrenamiento:")
        print(f"   Juegos jugados: {metrics['games_played']}")
        print(f"   Victorias: {metrics['wins']} ({metrics['win_rate']:.1%})")
        print(f"   Derrotas: {metrics['losses']}")
        print(f"   Empates: {metrics['draws']}")
        print(f"   Duración promedio: {metrics['avg_game_length']:.1f} movimientos")
        print(f"   Tamaño tabla Q: {metrics['q_table_size']} estados")
        print(f"   Epsilon actual: {metrics['current_epsilon']:.3f}")
        if metrics['training_duration'] > 0:
            print(f"   Tiempo entrenamiento: {metrics['training_duration']:.1f}s")

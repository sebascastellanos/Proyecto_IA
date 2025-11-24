#!/usr/bin/env python3
"""
🤖 Script de Entrenamiento Q-Learning para Connect 4
==================================================
Este script entrena un agente Q-Learning contra diferentes oponentes
y genera métricas detalladas del proceso de aprendizaje.
"""

import sys
import os
import numpy as np
import random
from datetime import datetime
import json

# Agregar rutas necesarias
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from learning.q_learning_agent import QLearningAgent
from connect4.policy import MCTSAgent
from connect4.connect_state import ConnectState
from connect4.environment_state import EnvironmentState

class TrainingEnvironment:
    """Entorno de entrenamiento para el agente Q-Learning"""
    
    def __init__(self):
        self.agents_trained = []
        
    def create_random_agent(self):
        """Crea un agente que juega aleatoriamente"""
        class RandomAgent:
            def act(self, state):
                if hasattr(state, 'valid_actions'):
                    valid_actions = state.valid_actions()
                else:
                    valid_actions = [col for col in range(7) if state.board[0][col] == 0]
                return random.choice(valid_actions) if valid_actions else 0
            
            def mount(self, timeout=None):
                pass
        
        return RandomAgent()
    
    def play_game(self, agent1, agent2, verbose=False):
        """Juega una partida entre dos agentes"""
        # Inicializar el estado del juego
        board = np.zeros((6, 7), dtype=int)
        current_player = 1  # Empieza el jugador 1
        moves_count = 0
        game_history = []
        
        while True:
            moves_count += 1
            state = ConnectState(board.copy())
            
            # Seleccionar agente actual
            if current_player == 1:
                current_agent = agent1
                player_symbol = 1
            else:
                current_agent = agent2
                player_symbol = -1
            
            # Obtener acción válida
            try:
                action = current_agent.act(state)
                if action not in state.valid_actions():
                    # Si la acción no es válida, elegir una aleatoria
                    action = random.choice(state.valid_actions())
            except Exception as e:
                if verbose:
                    print(f"Error en agente: {e}")
                action = random.choice(state.valid_actions())
            
            # Almacenar información para Q-Learning
            if hasattr(current_agent, 'training_metrics'):
                game_history.append({
                    'state': board.copy(),
                    'action': action,
                    'player': player_symbol
                })
            
            # Realizar movimiento
            board = self.make_move(board, action, player_symbol)
            
            # Verificar condiciones de victoria
            winner = self.check_winner(board)
            if winner != 0:
                # Juego terminado - alguien ganó
                if verbose:
                    print(f"🏆 Jugador {winner} gana en {moves_count} movimientos!")
                return winner, moves_count, game_history, board
            
            # Verificar empate
            if len([col for col in range(7) if board[0][col] == 0]) == 0:
                if verbose:
                    print(f"🤝 Empate después de {moves_count} movimientos")
                return 0, moves_count, game_history, board
            
            # Cambiar turno
            current_player *= -1
    
    def make_move(self, board, col, player):
        """Realiza un movimiento en el tablero"""
        board_copy = board.copy()
        for row in range(5, -1, -1):
            if board_copy[row][col] == 0:
                board_copy[row][col] = player
                break
        return board_copy
    
    def check_winner(self, board):
        """Verifica si hay un ganador"""
        # Verificar filas
        for row in range(6):
            for col in range(4):
                if (board[row][col] != 0 and
                    board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3]):
                    return board[row][col]
        
        # Verificar columnas
        for col in range(7):
            for row in range(3):
                if (board[row][col] != 0 and
                    board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col]):
                    return board[row][col]
        
        # Verificar diagonales
        for row in range(3):
            for col in range(4):
                if (board[row][col] != 0 and
                    board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]):
                    return board[row][col]
        
        for row in range(3, 6):
            for col in range(4):
                if (board[row][col] != 0 and
                    board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]):
                    return board[row][col]
        
        return 0
    
    def train_q_learning(self, episodes=1000, save_freq=100, opponents=['random', 'mcts']):
        """Entrena el agente Q-Learning"""
        print(f"🚀 Iniciando entrenamiento Q-Learning por {episodes} episodios...")
        
        # Crear agente Q-Learning
        q_agent = QLearningAgent(
            alpha=0.1,
            gamma=0.95,
            epsilon=1.0,
            epsilon_decay=0.995,
            epsilon_min=0.1,
            train_mode=True
        )
        q_agent.mount()
        
        # Crear oponentes
        opponents_pool = {}
        if 'random' in opponents:
            opponents_pool['Random'] = self.create_random_agent()
        if 'mcts' in opponents:
            mcts_agent = MCTSAgent()
            mcts_agent.mount()
            opponents_pool['MCTS'] = mcts_agent
        
        print(f"🎯 Oponentes: {list(opponents_pool.keys())}")
        
        # Entrenamiento
        checkpoint_data = []
        
        for episode in range(episodes):
            # Seleccionar oponente aleatoriamente
            opponent_name, opponent = random.choice(list(opponents_pool.items()))
            
            # Decidir quién juega primero (50/50)
            q_agent_goes_first = random.choice([True, False])
            
            if q_agent_goes_first:
                winner, moves, history, final_board = self.play_game(q_agent, opponent)
                q_agent_player = 1
            else:
                winner, moves, history, final_board = self.play_game(opponent, q_agent)
                q_agent_player = -1
            
            # Calcular recompensas y actualizar Q-Learning
            total_reward = 0
            if hasattr(q_agent, 'training_metrics'):
                for i, move_info in enumerate(history):
                    if move_info['player'] == q_agent_player:
                        # Calcular recompensa
                        if winner == q_agent_player:
                            reward = 10  # Victoria
                        elif winner == -q_agent_player:
                            reward = -10  # Derrota
                        else:
                            reward = 0  # Empate
                        
                        # Recompensa por movimiento (pequeña penalización por juegos largos)
                        reward += -0.1
                        
                        total_reward += reward
                        
                        # Actualizar Q-table (simplificado)
                        state_key = q_agent.get_state_key(move_info['state'])
                        if i < len(history) - 1:
                            next_state = history[i+1]['state'] if i+1 < len(history) else final_board
                            next_valid = [col for col in range(7) if next_state[0][col] == 0]
                            q_agent.update(move_info['state'], move_info['action'], reward, next_state, next_valid)
                
                # Actualizar métricas
                if winner == q_agent_player:
                    result = 'win'
                elif winner == -q_agent_player:
                    result = 'loss'
                else:
                    result = 'draw'
                
                q_agent.update_metrics(result, moves, total_reward)
            
            # Decay epsilon
            q_agent.decay_epsilon()
            
            # Checkpoint cada save_freq episodios
            if (episode + 1) % save_freq == 0:
                metrics = q_agent.get_metrics_report()
                checkpoint_data.append({
                    'episode': episode + 1,
                    'win_rate': metrics['win_rate'],
                    'epsilon': q_agent.epsilon,
                    'q_table_size': len(q_agent.q_table)
                })
                
                print(f"📊 Episodio {episode + 1}/{episodes}")
                print(f"   Win Rate: {metrics['win_rate']:.1%}")
                print(f"   Epsilon: {q_agent.epsilon:.3f}")
                print(f"   Q-Table: {len(q_agent.q_table)} estados")
                
                # Guardar progreso
                q_agent.save(f"models/q_agent_episode_{episode + 1}.pkl")
                q_agent.save_metrics(f"metrics/training_metrics_episode_{episode + 1}.json")
        
        # Entrenamiento completado
        print(f"\n✅ Entrenamiento completado!")
        q_agent.print_training_summary()
        
        # Guardar modelo final
        os.makedirs("models", exist_ok=True)
        os.makedirs("metrics", exist_ok=True)
        
        q_agent.save("models/q_agent_final.pkl")
        q_agent.save_metrics("metrics/training_metrics_final.json")
        
        # Guardar datos de checkpoints
        with open("metrics/checkpoint_data.json", "w") as f:
            json.dump(checkpoint_data, f, indent=2)
        
        return q_agent, checkpoint_data

def main():
    """Función principal"""
    print("🤖 Entrenamiento de Agente Q-Learning para Connect 4")
    print("=" * 50)
    
    # Crear entorno de entrenamiento
    env = TrainingEnvironment()
    
    # Configurar entrenamiento
    episodes = 2000
    save_frequency = 200
    opponents = ['random', 'mcts']
    
    print(f"⚙️ Configuración:")
    print(f"   Episodios: {episodes}")
    print(f"   Frecuencia guardado: cada {save_frequency} episodios")
    print(f"   Oponentes: {opponents}")
    print()
    
    # Ejecutar entrenamiento
    try:
        trained_agent, checkpoint_data = env.train_q_learning(
            episodes=episodes,
            save_freq=save_frequency,
            opponents=opponents
        )
        
        print(f"\n🎉 Entrenamiento exitoso!")
        print(f"📁 Archivos generados:")
        print(f"   - models/q_agent_final.pkl")
        print(f"   - metrics/training_metrics_final.json")
        print(f"   - metrics/checkpoint_data.json")
        
    except KeyboardInterrupt:
        print("\n⚠️ Entrenamiento interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante el entrenamiento: {e}")

if __name__ == "__main__":
    main()
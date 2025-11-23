import numpy as np
import random
from connect4.connect_state import ConnectState
from learning.q_learning_agent import QLearningAgent
from metrics.metrics_logger import log_metrics
import os

def get_reward(state, player):
    """Calcula la recompensa para un jugador dado el estado del juego"""
    winner = state.get_winner()
    if winner == player:
        return 1.0  # Victoria
    elif winner == -player:
        return -1.0  # Derrota
    elif winner == 0 and state.is_final():
        return 0.0  # Empate
    else:
        return 0.0  # Juego continúa

class RandomOpponent:
    """Oponente aleatorio para entrenar contra él"""
    def act(self, board):
        valid_actions = [c for c in range(7) if board[0, c] == 0]
        return random.choice(valid_actions) if valid_actions else 0

def train_q_learning_agent(episodes=1000, save_interval=100):
    """Entrena un agente Q-Learning contra un oponente aleatorio"""
    
    # Inicializar agente y oponente
    agent = QLearningAgent(alpha=0.1, gamma=0.95, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.1)
    opponent = RandomOpponent()
    
    # Contadores para métricas
    wins = 0
    losses = 0
    draws = 0
    
    print("🎯 Iniciando entrenamiento de Q-Learning...")
    print(f"Episodios totales: {episodes}")
    
    for episode in range(episodes):
        # Inicializar juego
        state = ConnectState()
        game_history = []
        total_reward = 0
        steps = 0
        
        # El agente puede ser jugador 1 o -1 aleatoriamente
        agent_player = random.choice([-1, 1])
        current_player = -1  # Siempre empieza el jugador -1
        
        while not state.is_final():
            steps += 1
            valid_actions = [c for c in range(7) if state.board[0, c] == 0]
            
            if current_player == agent_player:
                # Turno del agente Q-Learning
                board_state = state.board.copy()
                action = agent.choose_action(board_state, valid_actions)
                
                # Guardar estado-acción para actualizar después
                game_history.append({
                    'board': board_state,
                    'action': action,
                    'player': agent_player
                })
                
                # Ejecutar acción
                state = state.transition(action)
                
            else:
                # Turno del oponente aleatorio
                action = opponent.act(state.board)
                state = state.transition(action)
            
            current_player = -current_player
        
        # Juego terminado - calcular recompensas y actualizar Q-table
        final_reward = get_reward(state, agent_player)
        total_reward = final_reward
        
        # Actualizar estadísticas
        if final_reward > 0:
            wins += 1
        elif final_reward < 0:
            losses += 1
        else:
            draws += 1
        
        # Actualizar Q-table (experiencia replay simple)
        for i, experience in enumerate(game_history):
            board = experience['board']
            action = experience['action']
            
            # La recompensa es 0 para pasos intermedios, solo el resultado final cuenta
            if i == len(game_history) - 1:
                reward = final_reward
                next_board = state.board
                next_actions = []  # Estado final
            else:
                reward = 0.0
                next_experience = game_history[i + 1]
                next_board = next_experience['board']
                next_actions = [c for c in range(7) if next_board[0, c] == 0]
            
            agent.update(board, action, reward, next_board, next_actions)
        
        # Decay epsilon
        agent.decay_epsilon()
        
        # Log métricas cada cierto intervalo
        if (episode + 1) % save_interval == 0:
            avg_reward = total_reward
            win_rate = wins / (episode + 1) * 100
            
            log_metrics(episode + 1, avg_reward, steps, wins, losses, draws)
            
            print(f"Episodio {episode + 1:4d} | "
                  f"Win Rate: {win_rate:5.1f}% | "
                  f"Epsilon: {agent.epsilon:.3f} | "
                  f"Q-Table Size: {len(agent.q_table)}")
            
            # Guardar modelo cada cierto tiempo
            if (episode + 1) % (save_interval * 5) == 0:
                agent.save(f"metrics/q_table_episode_{episode + 1}.pkl")
    
    # Guardar modelo final
    agent.save("metrics/q_table.pkl")
    agent.save_q_table("metrics/q_table.npy")  # Para compatibilidad con QPolicy
    
    # Estadísticas finales
    print("\n🏆 Entrenamiento completado!")
    print(f"Victorias: {wins} ({wins/episodes*100:.1f}%)")
    print(f"Derrotas: {losses} ({losses/episodes*100:.1f}%)")
    print(f"Empates: {draws} ({draws/episodes*100:.1f}%)")
    print(f"Tamaño final de Q-table: {len(agent.q_table)} estados")
    print(f"Epsilon final: {agent.epsilon:.3f}")
    
    return agent

if __name__ == "__main__":
    # Crear directorio de métricas si no existe
    os.makedirs("metrics", exist_ok=True)
    
    # Entrenar el agente
    trained_agent = train_q_learning_agent(episodes=2000, save_interval=50)
    
    print("\n💾 Modelos guardados en:")
    print("  - metrics/q_table.pkl")
    print("  - metrics/q_table.npy")
    print("  - metrics/training_metrics.json")
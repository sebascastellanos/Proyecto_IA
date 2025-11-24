#!/usr/bin/env python3
"""
🎮 Proyecto de IA - Connect 4 Tournament
========================================

Este script principal permite ejecutar diferentes modos:
1. Entrenar agente Q-Learning
2. Ejecutar torneo entre agentes
3. Análisis de métricas
4. Juego individual entre dos agentes específicos

Autor: Proyecto IA
Fecha: Noviembre 2025
"""

import os
import sys
import argparse

# Agregar el directorio tournament al path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'tournament'))

def train_q_learning():
    """Entrena el agente Q-Learning"""
    print(" Iniciando entrenamiento Q-Learning...")
    
    # Verificar si estamos en el directorio correcto
    if not os.path.exists('tournament'):
        print(" No se encuentra el directorio 'tournament'. Asegúrate de ejecutar desde la raíz del proyecto.")
        return
    
    # Cambiar al directorio tournament temporalmente
    original_dir = os.getcwd()
    try:
        os.chdir('tournament')
        from train_q_learning import train_q_learning_agent
        train_q_learning_agent(episodes=2000, save_interval=100)
        print(" Entrenamiento completado!")
    except Exception as e:
        print(f"Error durante el entrenamiento: {e}")
    finally:
        os.chdir(original_dir)

def run_tournament():
    """Ejecuta el torneo entre todos los agentes"""
    print("🏆 Iniciando torneo...")
    
    # Verificar directorio
    if not os.path.exists('tournament'):
        print(" No se encuentra el directorio 'tournament'. Asegúrate de ejecutar desde la raíz del proyecto.")
        return
    
    # Ejecutar desde el subdirectorio tournament
    original_dir = os.getcwd()
    try:
        os.chdir('tournament')
        os.system('python main.py --mode tournament')
        print(" Torneo completado!")
    finally:
        os.chdir(original_dir)

def analyze_metrics():
    """Abre el análisis de métricas en Jupyter"""
    print(" Abriendo análisis de métricas...")
    
    # Verificar directorio
    if not os.path.exists('tournament/metrics'):
        print(" No se encuentra el directorio 'tournament/metrics'.")
        return
    
    original_dir = os.getcwd()
    try:
        os.chdir('tournament')
        print(" Ejecutando: jupyter notebook metrics/metrics_analisys.ipynb")
        os.system('jupyter notebook metrics/metrics_analisys.ipynb')
    finally:
        os.chdir(original_dir)

def play_custom_match():
    """Permite jugar un match customizado entre dos agentes"""
    print(" Match personalizado...")
    
    if not os.path.exists('tournament'):
        print("No se encuentra el directorio 'tournament'.")
        return
    
    original_dir = os.getcwd()
    try:
        os.chdir('tournament')
        
        print("Agentes disponibles:")
        print("1. MCTS Agent")
        print("2. Q-Learning Agent")
        print("3. Random Agent")
        
        from connect4.policy import MCTSAgent, QPolicy
        from tournament import play
        
        # Para simplificar, haremos MCTS vs Q-Learning
        mcts = ("MCTS-Agent", MCTSAgent)
        q_agent = ("Q-Agent", QPolicy)
        
        winner = play(mcts, q_agent, best_of=5, first_player_distribution=0.5)
        print(f"Ganador: {winner[0]}")
    except Exception as e:
        print(f"Error en match personalizado: {e}")
    finally:
        os.chdir(original_dir)

def main():
    parser = argparse.ArgumentParser(description=" Proyecto IA - Connect 4")
    parser.add_argument('--mode', choices=['train', 'tournament', 'metrics', 'play'], 
                       default='tournament',
                       help='Modo de ejecución')
    
    args = parser.parse_args()
    
    print("=" * 50)
    print(" PROYECTO IA - CONNECT 4")
    print("=" * 50)
    
    if args.mode == 'train':
        train_q_learning()
    elif args.mode == 'tournament':
        run_tournament()
    elif args.mode == 'metrics':
        analyze_metrics()
    elif args.mode == 'play':
        play_custom_match()
    
    print("\n Ejecución completada!")

if __name__ == "__main__":
    main()
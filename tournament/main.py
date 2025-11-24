#!/usr/bin/env python3
"""
🏆 Connect 4 Tournament Main Script
==================================
Este es el script principal del torneo.
Ejecuta el torneo entre todos los agentes.
"""

import argparse
from connect4.base_policy import Policy
from connect4.utils import find_importable_classes
from tournament import run_tournament, play

def run_tournament_main():
    """Ejecuta el torneo principal"""
    print("🏆 Iniciando torneo entre agentes...")
    
    try:
        # Read all files within subfolder of "groups"
        participants = find_importable_classes("groups", Policy)
        
        print(f"🔍 Agentes detectados: {list(participants.keys())}")
        
        # Build a participant list (name, class)
        players = list(participants.items())
        
        if len(players) == 0:
            print("⚠️ No se encontraron agentes en el directorio 'groups'")
            print("💡 Asegúrate de que:")
            print("   - Los archivos policy.py existan en cada subdirectorio de groups/")
            print("   - Las clases hereden de Policy")
            print("   - No haya errores de importación")
            return
        
        print(f"📋 Participantes del torneo: {[name for name, _ in players]}")
        
        # Add our own implemented agents to make the tournament more interesting
        from connect4.policy import MCTSAgent
        
        # Add MCTS agent
        players.append(("MCTS-Champion", MCTSAgent))
        
        # Try to add Q-Learning agent if available
        try:
            from connect4.policy import QPolicy
            players.append(("Q-Learning-AI", QPolicy))
            print("✅ Agente Q-Learning añadido al torneo")
        except Exception as e:
            print(f"⚠️ No se pudo cargar Q-Learning agent: {e}")
        
        print(f"🎯 Total de participantes: {len(players)}")
        
        # Run the tournament
        champion = run_tournament(
            players,
            play,  # You could also create your own play function for testing purposes
            shuffle=True,
        )
        
        print(f"\n🏆 ¡Campeón del torneo: {champion[0]}!")
        return champion
        
    except Exception as e:
        print(f"❌ Error ejecutando el torneo: {e}")
        import traceback
        traceback.print_exc()
        return None

def train_q_learning():
    """Entrena el agente Q-Learning"""
    print("🚀 Iniciando entrenamiento Q-Learning...")
    try:
        from train_q_learning import train_q_learning_agent
        train_q_learning_agent(episodes=2000, save_interval=100)
        print("✅ Entrenamiento completado!")
    except ImportError as e:
        print(f"❌ Error al importar módulo de entrenamiento: {e}")
    except Exception as e:
        print(f"❌ Error durante el entrenamiento: {e}")

def analyze_metrics():
    """Abre el análisis de métricas"""
    print("📊 Para analizar métricas, abre el notebook:")
    print("   jupyter notebook metrics/metrics_analisys.ipynb")

def test_agents():
    """Prueba rápida entre dos agentes específicos"""
    print("🎯 Prueba rápida entre agentes...")
    
    try:
        from connect4.policy import MCTSAgent
        
        # Crear dos instancias del mismo agente para testing
        players = [
            ("MCTS-A", MCTSAgent),
            ("MCTS-B", MCTSAgent),
        ]
        
        print("🥊 Match de prueba: MCTS-A vs MCTS-B")
        winner = play(players[0], players[1], best_of=3, first_player_distribution=0.5)
        print(f"🏆 Ganador del test: {winner[0]}")
        
    except Exception as e:
        print(f"❌ Error en test de agentes: {e}")

def main():
    parser = argparse.ArgumentParser(description="🎮 Connect 4 Tournament")
    parser.add_argument('--mode', choices=['tournament', 'train', 'metrics', 'test'], 
                       default='tournament',
                       help='Modo de ejecución')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🎮 CONNECT 4 TOURNAMENT")
    print("=" * 60)
    
    if args.mode == 'tournament':
        run_tournament_main()
    elif args.mode == 'train':
        train_q_learning()
    elif args.mode == 'metrics':
        analyze_metrics()
    elif args.mode == 'test':
        test_agents()
    
    print("\n✨ Ejecución completada!")

if __name__ == "__main__":
    # Modo legacy - ejecutar torneo directamente si no se especifican argumentos
    import sys
    if len(sys.argv) == 1:
        run_tournament_main()
    else:
        main()
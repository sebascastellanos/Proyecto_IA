#!/usr/bin/env python3
"""
📊 Análisis de Métricas de Entrenamiento Q-Learning
==================================================
Script para analizar y visualizar las métricas de entrenamiento
del agente Q-Learning.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import sys

# Configurar estilo de gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class MetricsAnalyzer:
    """Analizador de métricas de entrenamiento"""
    
    def __init__(self, metrics_file='metrics/training_metrics_final.json'):
        self.metrics_file = metrics_file
        self.metrics = None
        self.load_metrics()
    
    def load_metrics(self):
        """Carga las métricas desde el archivo JSON"""
        try:
            with open(self.metrics_file, 'r') as f:
                self.metrics = json.load(f)
            print(f"✅ Métricas cargadas desde {self.metrics_file}")
        except FileNotFoundError:
            print(f"❌ No se encontró el archivo {self.metrics_file}")
            self.metrics = None
        except Exception as e:
            print(f"❌ Error cargando métricas: {e}")
            self.metrics = None
    
    def print_summary(self):
        """Imprime un resumen de las métricas"""
        if not self.metrics:
            print("❌ No hay métricas disponibles")
            return
        
        print("\\n🎯 RESUMEN DE ENTRENAMIENTO")
        print("=" * 50)
        print(f"📊 Juegos totales: {self.metrics.get('games_played', 0)}")
        print(f"🏆 Victorias: {self.metrics.get('wins', 0)}")
        print(f"💔 Derrotas: {self.metrics.get('losses', 0)}")
        print(f"🤝 Empates: {self.metrics.get('draws', 0)}")
        print(f"📈 Tasa de victoria: {self.metrics.get('win_rate', 0):.1%}")
        print(f"⏱️  Duración promedio: {self.metrics.get('avg_game_length', 0):.1f} movimientos")
        print(f"🧠 Tamaño tabla Q: {self.metrics.get('q_table_size', 0)} estados")
        print(f"🎲 Epsilon final: {self.metrics.get('current_epsilon', 0):.3f}")
        print(f"⚡ Tasa de aprendizaje: {self.metrics.get('learning_rate', 0):.3f}")
        print(f"💰 Factor de descuento: {self.metrics.get('discount_factor', 0):.3f}")
        
        if self.metrics.get('training_duration'):
            duration = self.metrics['training_duration']
            print(f"⏰ Tiempo de entrenamiento: {duration:.1f}s ({duration/60:.1f} min)")
        
        # Estadísticas avanzadas
        if self.metrics.get('game_lengths'):
            lengths = self.metrics['game_lengths']
            print(f"\\n📏 ESTADÍSTICAS DE DURACIÓN:")
            print(f"   Min: {min(lengths)} movimientos")
            print(f"   Max: {max(lengths)} movimientos")
            print(f"   Mediana: {np.median(lengths):.1f} movimientos")
            print(f"   Desv. estándar: {np.std(lengths):.1f}")
        
        if self.metrics.get('rewards_per_game'):
            rewards = self.metrics['rewards_per_game']
            print(f"\\n💎 ESTADÍSTICAS DE RECOMPENSAS:")
            print(f"   Promedio: {np.mean(rewards):.2f}")
            print(f"   Min: {min(rewards):.2f}")
            print(f"   Max: {max(rewards):.2f}")
            print(f"   Desv. estándar: {np.std(rewards):.2f}")
    
    def plot_training_progress(self):
        """Genera gráficos del progreso de entrenamiento"""
        if not self.metrics:
            print("❌ No hay métricas disponibles para graficar")
            return
        
        # Crear directorio de gráficos
        os.makedirs('plots', exist_ok=True)
        
        # Configurar subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('📊 Análisis de Entrenamiento Q-Learning Connect 4', fontsize=16, fontweight='bold')
        
        # 1. Evolución de Epsilon (Exploración)
        if self.metrics.get('epsilon_history'):
            epsilon_history = self.metrics['epsilon_history']
            axes[0, 0].plot(epsilon_history, color='blue', linewidth=2)
            axes[0, 0].set_title('🎲 Evolución de Epsilon (Exploración)')
            axes[0, 0].set_xlabel('Episodios')
            axes[0, 0].set_ylabel('Epsilon')
            axes[0, 0].grid(True, alpha=0.3)
            axes[0, 0].set_ylim(0, 1.05)
        
        # 2. Distribución de duración de juegos
        if self.metrics.get('game_lengths'):
            game_lengths = self.metrics['game_lengths']
            axes[0, 1].hist(game_lengths, bins=30, alpha=0.7, color='green', edgecolor='black')
            axes[0, 1].set_title('📏 Distribución de Duración de Juegos')
            axes[0, 1].set_xlabel('Número de Movimientos')
            axes[0, 1].set_ylabel('Frecuencia')
            axes[0, 1].grid(True, alpha=0.3)
            axes[0, 1].axvline(np.mean(game_lengths), color='red', linestyle='--', 
                              label=f'Promedio: {np.mean(game_lengths):.1f}')
            axes[0, 1].legend()
        
        # 3. Distribución de recompensas
        if self.metrics.get('rewards_per_game'):
            rewards = self.metrics['rewards_per_game']
            axes[1, 0].hist(rewards, bins=30, alpha=0.7, color='orange', edgecolor='black')
            axes[1, 0].set_title('💎 Distribución de Recompensas por Juego')
            axes[1, 0].set_xlabel('Recompensa Total')
            axes[1, 0].set_ylabel('Frecuencia')
            axes[1, 0].grid(True, alpha=0.3)
            axes[1, 0].axvline(np.mean(rewards), color='red', linestyle='--',
                              label=f'Promedio: {np.mean(rewards):.2f}')
            axes[1, 0].legend()
        
        # 4. Resumen de resultados
        wins = self.metrics.get('wins', 0)
        losses = self.metrics.get('losses', 0)
        draws = self.metrics.get('draws', 0)
        
        if wins + losses + draws > 0:
            labels = ['Victorias', 'Derrotas', 'Empates']
            sizes = [wins, losses, draws]
            colors = ['#2ecc71', '#e74c3c', '#f39c12']
            
            # Filtrar valores que son 0
            filtered_data = [(label, size, color) for label, size, color in zip(labels, sizes, colors) if size > 0]
            if filtered_data:
                labels, sizes, colors = zip(*filtered_data)
                
                wedges, texts, autotexts = axes[1, 1].pie(sizes, labels=labels, autopct='%1.1f%%', 
                                                         colors=colors, startangle=90)
                axes[1, 1].set_title('🏆 Distribución de Resultados')
                
                # Mejorar apariencia del texto
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
        
        plt.tight_layout()
        plt.savefig('plots/training_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("📁 Gráfico guardado en: plots/training_analysis.png")
    
    def plot_learning_curve(self, checkpoint_file='metrics/checkpoint_data.json'):
        """Grafica la curva de aprendizaje usando datos de checkpoints"""
        try:
            with open(checkpoint_file, 'r') as f:
                checkpoint_data = json.load(f)
        except FileNotFoundError:
            print(f"❌ No se encontró {checkpoint_file}")
            return
        
        if not checkpoint_data:
            print("❌ No hay datos de checkpoints disponibles")
            return
        
        episodes = [cp['episode'] for cp in checkpoint_data]
        win_rates = [cp['win_rate'] for cp in checkpoint_data]
        epsilons = [cp['epsilon'] for cp in checkpoint_data]
        q_sizes = [cp['q_table_size'] for cp in checkpoint_data]
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        fig.suptitle('📈 Curva de Aprendizaje Q-Learning', fontsize=16, fontweight='bold')
        
        # 1. Tasa de victoria a lo largo del tiempo
        axes[0].plot(episodes, [wr * 100 for wr in win_rates], marker='o', linewidth=2, markersize=4)
        axes[0].set_title('🏆 Evolución Tasa de Victoria')
        axes[0].set_xlabel('Episodios')
        axes[0].set_ylabel('Tasa de Victoria (%)')
        axes[0].grid(True, alpha=0.3)
        axes[0].set_ylim(0, 100)
        
        # 2. Epsilon vs Episodios
        axes[1].plot(episodes, epsilons, marker='s', linewidth=2, markersize=4, color='orange')
        axes[1].set_title('🎲 Decay de Exploración (Epsilon)')
        axes[1].set_xlabel('Episodios')
        axes[1].set_ylabel('Epsilon')
        axes[1].grid(True, alpha=0.3)
        axes[1].set_ylim(0, 1)
        
        # 3. Crecimiento de la tabla Q
        axes[2].plot(episodes, q_sizes, marker='^', linewidth=2, markersize=4, color='green')
        axes[2].set_title('🧠 Crecimiento Tabla Q')
        axes[2].set_xlabel('Episodios')
        axes[2].set_ylabel('Estados en Tabla Q')
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('plots/learning_curve.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("📁 Curva de aprendizaje guardada en: plots/learning_curve.png")
    
    def generate_report(self):
        """Genera un reporte completo en texto"""
        if not self.metrics:
            print("❌ No hay métricas disponibles para el reporte")
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
🤖 REPORTE DE ENTRENAMIENTO Q-LEARNING CONNECT 4
===============================================
Generado el: {timestamp}

CONFIGURACIÓN DEL AGENTE:
- Tasa de aprendizaje (α): {self.metrics.get('learning_rate', 'N/A')}
- Factor de descuento (γ): {self.metrics.get('discount_factor', 'N/A')}
- Epsilon inicial: 1.0
- Epsilon final: {self.metrics.get('current_epsilon', 'N/A'):.3f}
- Epsilon mínimo: 0.1

RESULTADOS DEL ENTRENAMIENTO:
- Juegos totales jugados: {self.metrics.get('games_played', 0)}
- Victorias: {self.metrics.get('wins', 0)} ({self.metrics.get('win_rate', 0):.1%})
- Derrotas: {self.metrics.get('losses', 0)}
- Empates: {self.metrics.get('draws', 0)}
- Duración promedio: {self.metrics.get('avg_game_length', 0):.1f} movimientos

APRENDIZAJE:
- Estados explorados: {self.metrics.get('q_table_size', 0)}
- Recompensa promedio por episodio: {self.metrics.get('avg_reward_per_episode', 0):.2f}
"""
        
        if self.metrics.get('training_duration'):
            duration = self.metrics['training_duration']
            report += f"- Tiempo total de entrenamiento: {duration:.1f}s ({duration/60:.1f} minutos)\\n"
        
        # Estadísticas adicionales
        if self.metrics.get('game_lengths'):
            lengths = self.metrics['game_lengths']
            report += f"""
ANÁLISIS ESTADÍSTICO:
- Duración mínima: {min(lengths)} movimientos
- Duración máxima: {max(lengths)} movimientos
- Mediana de duración: {np.median(lengths):.1f} movimientos
- Desviación estándar: {np.std(lengths):.1f}
"""
        
        if self.metrics.get('rewards_per_game'):
            rewards = self.metrics['rewards_per_game']
            report += f"""
ANÁLISIS DE RECOMPENSAS:
- Recompensa mínima: {min(rewards):.2f}
- Recompensa máxima: {max(rewards):.2f}
- Desviación estándar: {np.std(rewards):.2f}
"""
        
        report += f"""
CONCLUSIONES:
- El agente alcanzó una tasa de victoria del {self.metrics.get('win_rate', 0):.1%}
- Se exploraron {self.metrics.get('q_table_size', 0)} estados únicos del juego
- La exploración se redujo gradualmente de 100% a {self.metrics.get('current_epsilon', 0)*100:.1f}%

===============================================
"""
        
        # Guardar reporte
        os.makedirs('reports', exist_ok=True)
        report_file = f"reports/training_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(report)
        print(f"📁 Reporte guardado en: {report_file}")

def main():
    """Función principal"""
    print("📊 Análisis de Métricas de Entrenamiento Q-Learning")
    print("=" * 50)
    
    # Crear analizador
    analyzer = MetricsAnalyzer()
    
    if analyzer.metrics:
        # Imprimir resumen
        analyzer.print_summary()
        
        # Generar gráficos
        print("\\n🎨 Generando visualizaciones...")
        analyzer.plot_training_progress()
        analyzer.plot_learning_curve()
        
        # Generar reporte completo
        print("\\n📝 Generando reporte completo...")
        analyzer.generate_report()
        
        print("\\n✅ Análisis completado!")
        print("📁 Revisa las carpetas 'plots' y 'reports' para los resultados")
    else:
        print("❌ No se pudieron cargar las métricas. ¿Ya entrenaste el agente?")
        print("💡 Ejecuta primero: python train_agent.py")

if __name__ == "__main__":
    main()
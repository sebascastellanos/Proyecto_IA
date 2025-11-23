# 🎮 Connect 4 AI Tournament

Un proyecto completo de Inteligencia Artificial que implementa diferentes agentes para jugar Connect 4 y los enfrenta en un torneo eliminatorio.

## 🚀 Características

### 🤖 Agentes Implementados

1. **MCTS Agent** - Monte Carlo Tree Search
   - Implementación completa con UCB1
   - Heurísticas de victoria inmediata y bloqueo
   - Rollouts limitados para optimización
   - Selección hacia el centro en empates

2. **Q-Learning Agent** - Aprendizaje por Refuerzo
   - Tabla Q para aprendizaje de estados
   - Exploración epsilon-greedy con decay
   - Entrenamiento contra oponente aleatorio
   - Métricas de entrenamiento detalladas

3. **Random Agents** - Baseline
   - Diferentes implementaciones aleatorias
   - Útiles para testing y baseline

### 🏆 Sistema de Torneo

- **Torneo eliminatorio** con emparejamientos automáticos
- **Manejo de BYEs** para números impares de participantes
- **Guardado automático** de todos los matches en JSON
- **Configuración flexible** (best_of, distribución de primer jugador, etc.)

### 📊 Métricas y Análisis

- **Logging automático** durante entrenamiento
- **Visualizaciones** de progreso de aprendizaje
- **Análisis estadístico** de rendimiento
- **Jupyter notebook** para análisis interactivo

## 📁 Estructura del Proyecto

```
Proyecto_IA/
├── main.py                     # Script principal
├── Informe.ipynb              # Informe del proyecto
└── tournament/
    ├── main.py                # Ejecutor del torneo
    ├── tournament.py          # Lógica del torneo
    ├── train_q_learning.py    # Script de entrenamiento
    ├── connect4/              # Core del juego
    │   ├── connect_state.py   # Estado del juego
    │   ├── policy.py          # Políticas/Agentes
    │   ├── dtos.py           # Estructuras de datos
    │   └── utils.py          # Utilidades
    ├── learning/              # Módulos de aprendizaje
    │   └── q_learning_agent.py
    ├── metrics/               # Métricas y análisis
    │   ├── metrics_logger.py
    │   └── metrics_analisys.ipynb
    ├── groups/                # Agentes participantes
    │   ├── Group A/
    │   ├── Group B/
    │   └── Group C/
    └── versus/                # Resultados de matches
        └── *.json
```

## 🛠️ Instalación

```bash
# Clonar el repositorio
git clone <repository-url>
cd Proyecto_IA

# Instalar dependencias
pip install numpy matplotlib pydantic jupyter
```

## 🚀 Uso

### Modo Rápido

```bash
# Entrenar Q-Learning y ejecutar torneo
python main.py --mode train
python main.py --mode tournament
```

### Modo Detallado

1. **Entrenar el agente Q-Learning:**
```bash
python main.py --mode train
# O directamente:
cd tournament
python train_q_learning.py
```

2. **Ejecutar torneo:**
```bash
python main.py --mode tournament
# O directamente:
cd tournament
python main.py
```

3. **Analizar métricas:**
```bash
python main.py --mode metrics
# O abrir directamente:
jupyter notebook tournament/metrics/metrics_analisys.ipynb
```

4. **Match personalizado:**
```bash
python main.py --mode play
```

## 📊 Interpretación de Resultados

### Métricas de Entrenamiento

- **Tasa de Victoria**: Porcentaje de partidas ganadas vs oponente aleatorio
- **Recompensas**: Evolución del aprendizaje (1=victoria, -1=derrota, 0=empate)
- **Duración de Partidas**: Número de movimientos por partida
- **Progreso Acumulado**: Victorias, derrotas y empates totales

### Resultados del Torneo

Los archivos en `tournament/versus/` contienen:
- **Estadísticas del match**: victorias, derrotas, empates
- **Historia completa**: cada movimiento de cada partida
- **Formato JSON**: fácil análisis posterior

## 🔧 Configuración

### Parámetros del Q-Learning

En `train_q_learning.py`:
- `episodes`: Número de partidas de entrenamiento (default: 2000)
- `alpha`: Tasa de aprendizaje (default: 0.1)
- `gamma`: Factor de descuento (default: 0.95)
- `epsilon_decay`: Decaimiento de exploración (default: 0.995)

### Parámetros del MCTS

En `connect4/policy.py`:
- `iterations`: Simulaciones por movimiento (default: 400)
- `c`: Parámetro de exploración UCB1 (default: 1.4)
- `rollout_limit`: Límite de pasos por rollout (default: 100)

### Parámetros del Torneo

En `tournament.py`:
- `best_of`: Partidas por match (default: 7)
- `first_player_distribution`: Proporción de partidas como primer jugador (default: 0.5)
- `shuffle`: Mezclar emparejamientos iniciales (default: True)

## 🧪 Testing

```bash
# Test rápido con pocos episodios
cd tournament
python -c "from train_q_learning import train_q_learning_agent; train_q_learning_agent(episodes=100)"

# Test de torneo con agentes simples
python tournament.py
```

## 📈 Optimización de Rendimiento

### Para Q-Learning:
- Aumentar `episodes` para mejor aprendizaje
- Ajustar `alpha` según velocidad de convergencia
- Modificar `epsilon_decay` para balance exploración/explotación

### Para MCTS:
- Aumentar `iterations` para mejor juego (más lento)
- Ajustar `c` para balance exploración/explotación
- Modificar `rollout_limit` según recursos computacionales

## 🐛 Troubleshooting

### Problemas Comunes:

1. **"No module found"**: Asegúrate de estar en el directorio correcto
2. **"No se encontró q_table"**: Ejecuta primero el entrenamiento
3. **"Memoria insuficiente"**: Reduce `episodes` o `iterations`
4. **"Partidas muy lentas"**: Reduce `iterations` del MCTS

### Logs y Debug:

- Los entrenamientos muestran progreso cada 50-100 episodios
- Los matches se guardan automáticamente en `versus/`
- Las métricas se registran en `metrics/training_metrics.json`

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🎯 Próximas Mejoras

- [ ] Implementar agente basado en redes neuronales
- [ ] Añadir más oponentes para entrenamiento
- [ ] Optimizar representación de estado para Q-Learning
- [ ] Implementar aprendizaje multi-agente
- [ ] Añadir interfaz gráfica para juego humano vs IA
- [ ] Paralelización del entrenamiento

---

**¡Buena suerte en el torneo! 🏆**
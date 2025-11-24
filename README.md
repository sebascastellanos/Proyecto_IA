
# Connect 4 AI Tournament

Proyecto completo de Inteligencia Artificial para el juego Connect 4, que integra distintos agentes autónomos y los enfrenta en un torneo eliminatorio. El desarrollo incluye agentes basados en búsqueda, aprendizaje por refuerzo y estrategias aleatorias, así como módulos de análisis, métricas y herramientas para la ejecución de torneos.

## 1. Características del Proyecto

### 1.1 Agentes Implementados

**1. MCTS Agent (Monte Carlo Tree Search)**

* Implementación basada en UCT (Upper Confidence Bounds applied to Trees).
* Incluye heurísticas simples, como detección de victoria inmediata y bloqueo del oponente.
* Rollouts aleatorios con límite de pasos para mejorar la eficiencia.
* Política de desempate inclinada hacia columnas centrales.
* Parámetros ajustables: número de iteraciones (por defecto 400), constante de exploración (1.4) y límite de rollout (100).

**2. Q-Learning Agent**

* Implementación basada en tabla Q para aprendizaje por refuerzo.
* Estrategia epsilon-greedy con decaimiento progresivo.
* Entrenamiento contra oponente aleatorio.
* Registro y análisis detallado de métricas de entrenamiento.

**3. Random Agents**

* Diferentes políticas aleatorias empleadas como baseline o para pruebas de rendimiento.

### 1.2 Sistema de Torneo

* Torneo eliminatorio con emparejamientos automáticos.
* Manejo automático de participantes impares mediante BYEs.
* Registro completo en formato JSON de cada match.
* Parámetros configurables, como cantidad de partidas por enfrentamiento y distribución del primer jugador.

### 1.3 Métricas y Análisis

* Registro automático de métricas durante el entrenamiento.
* Visualización del progreso del aprendizaje mediante notebooks.
* Estadísticas de rendimiento de todos los agentes.
* Herramientas interactivas para análisis en Jupyter.

## 2. Estructura del Proyecto

```
Proyecto_IA/
├── main.py
├── Informe.ipynb
└── tournament/
    ├── main.py
    ├── tournament.py
    ├── train_q_learning.py
    ├── connect4/
    │   ├── connect_state.py
    │   ├── policy.py
    │   ├── dtos.py
    │   └── utils.py
    ├── learning/
    │   └── q_learning_agent.py
    ├── metrics/
    │   ├── metrics_logger.py
    │   └── metrics_analisys.ipynb
    ├── groups/
    │   ├── Group A/
    │   ├── Group B/
    │   └── Group C/
    └── versus/
        └── *.json
```

## 3. Instalación

```
git clone <repository-url>
cd Proyecto_IA
pip install numpy matplotlib pydantic jupyter
```

## 4. Ejecución

### 4.1 Modo rápido

```
python main.py --mode train
python main.py --mode tournament
```

### 4.2 Modo detallado

**Entrenamiento del agente Q-Learning**

```
python main.py --mode train
```

O directamente:

```
cd tournament
python train_q_learning.py
```

**Ejecución del torneo**

```
python main.py --mode tournament
```

O:

```
cd tournament
python main.py
```

**Análisis de métricas**

```
python main.py --mode metrics
```

O abrir el notebook:

```
jupyter notebook tournament/metrics/metrics_analisys.ipynb
```

**Ejecución de un match personalizado**

```
python main.py --mode play
```

## 5. Interpretación de Resultados

### 5.1 Métricas de Entrenamiento

* Porcentaje de victorias frente a un oponente aleatorio.
* Evolución de recompensas acumuladas.
* Duración promedio de las partidas.
* Evolución de victorias, derrotas y empates.

### 5.2 Resultados del Torneo

Los archivos JSON en `tournament/versus/` incluyen:

* Estadísticas completas del match.
* Secuencia de movimientos.
* Número de victorias, empates y derrotas por enfrentamiento.

## 6. Configuración

### 6.1 Parámetros del Q-Learning

Definidos en `train_q_learning.py`:

* `episodes` (por defecto 2000)
* `alpha = 0.1`
* `gamma = 0.95`
* `epsilon_decay = 0.995`

### 6.2 Parámetros del MCTS

Definidos en `connect4/policy.py`:

* `iterations = 400`
* `c = 1.4`
* `rollout_limit = 100`

### 6.3 Parámetros del Torneo

Definidos en `tournament.py`:

* `best_of = 7`
* `first_player_distribution = 0.5`
* `shuffle = True`

## 7. Pruebas y Debugging

### Pruebas rápidas

```
cd tournament
python -c "from train_q_learning import train_q_learning_agent; train_q_learning_agent(episodes=100)"
```

### Torneo básico

```
python tournament.py
```

### Problemas comunes

1. Error de módulos: ejecutar desde el directorio raíz del proyecto.
2. Falta de archivo de tabla Q: es necesario entrenar primero.
3. Uso excesivo de memoria: reducir episodios o iteraciones.
4. Partidas lentas: disminuir iteraciones en MCTS.

## 8. Optimización

### Para Q-Learning

* Incrementar episodios de entrenamiento.
* Ajustar tasa de aprendizaje según estabilidad.
* Modificar el decaimiento de epsilon para equilibrar exploración y explotación.

### Para MCTS

* Aumentar iteraciones cuando se requiere mayor calidad de juego.
* Ajustar la constante de exploración para estabilizar decisiones.
* Optimizar el límite de rollout según disponibilidad de cómputo.

## 9. Contribución

1. Crear un fork del proyecto.
2. Crear una rama para la nueva funcionalidad.
3. Realizar commits con descripciones claras.
4. Hacer push de los cambios.
5. Abrir un Pull Request con la explicación correspondiente.

## 10. Licencia

Proyecto distribuido bajo licencia MIT. Para más detalles, consultar el archivo `LICENSE`.

## 11. Próximas Mejoras

* Implementación de un agente basado en redes neuronales.
* Inclusión de más oponentes para entrenamiento.
* Optimización de la representación del estado en Q-Learning.
* Entrenamiento multi-agente.
* Desarrollo de una interfaz gráfica para interacción humano-IA.
* Paralelización del proceso de entrenamiento.

--
import numpy as np
from connect4.policy import Policy
from connect4.utils import get_valid_moves
from typing import Dict
import hashlib
from abc import ABC, abstractmethod


#definimos el agente que heredará de policy
class UCB1Agent(Policy):
    #inicializamos los contadores y valores Q
    def __init__(self):
        # Mapeos: estado_hash → [Q(s,a), N(s), N(s,a)]
        #guarda las rescompensas promedio por acción en cada estado
        self.Q: Dict[str, Dict[int, float]] = {}
        #total de veces que se ha visitado cada estado 
        self.N: Dict[str, int] = {}
        #veces que se ha ejecutado una acción especifica a en ese estado
        self.N_a: Dict[str, Dict[int, int]] = {}
        self.c = 1.4  # constante de exploración

    def mount(self) -> None:
        #Inicializa estructuras si es necesario al comienzo del torneo
        pass  # Nada que hacer aquí todavía

    def act(self, s: np.ndarray) -> int:
        #Elige la mejor acción usando UCB1 para un estado dado
        state_hash = self._hash_state(s)
        valid_moves = get_valid_moves(s)

        # Inicialización si no hemos visto este estado
        if state_hash not in self.Q:
            self.Q[state_hash] = {a: 0.0 for a in valid_moves}
            self.N_a[state_hash] = {a: 0 for a in valid_moves}
            self.N[state_hash] = 0

        # Recuperar datos
        q = self.Q[state_hash]
        n_a = self.N_a[state_hash]
        N = self.N[state_hash]

        # Cálculo UCB1
        ucb_scores = {}
        for a in valid_moves:
            if n_a[a] == 0:
                ucb_scores[a] = float("inf")  # explorar acciones no jugadas
            else:
                ucb_scores[a] = q[a] + self.c * np.sqrt(np.log(N + 1) / n_a[a])

        # Escoger acción con mayor UCB1
        best_action = max(ucb_scores, key=ucb_scores.get)

        # Actualizar conteo de visitas
        self.N[state_hash] += 1
        self.N_a[state_hash][best_action] += 1

        return best_action

    def _hash_state(self, s: np.ndarray) -> str:
        """Hash simple del estado como string para usar como clave"""
        return hashlib.md5(s.tobytes()).hexdigest()
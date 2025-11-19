import numpy as np
from connect4.policy import Policy

# Constantes para el juego de Conecta-4
ROWS, COLS = 6, 7              # Tablero de 6 filas x 7 columnas
EMPTY, P1, P2 = 0, -1, 1       # Estados de cada celda: vacía, jugador 1, jugador 2

# Clase del agente, hereda de Policy (interfaz esperada por el entorno)
class UCB1Agent(Policy):

    def __init__(self, depth: int = 3):
        # Profundidad de búsqueda del algoritmo Minimax
        self.depth = depth

    def mount(self):
        # Método requerido por el entorno, pero no se usa en esta implementación
        pass

    def act(self, s):
        # Convierte el estado en matriz de numpy, dependiendo del formato que tenga
        board = s.board if hasattr(s, 'board') else np.array(s)

        # Obtiene las columnas válidas donde se puede jugar (las que no están llenas)
        valid = s.valid_actions() if hasattr(s, 'valid_actions') else [c for c in range(COLS) if board[0, c] == EMPTY]
        if not valid:
            return 0  # Caso extremo donde no hay jugadas válidas

        # Determina qué jugador tiene el turno (basado en la cantidad de fichas ya jugadas)
        p_turn = P1 if np.count_nonzero(board == P1) == np.count_nonzero(board == P2) else P2
        opp = -p_turn  # El oponente es el opuesto del jugador actual

        # 1. Si el jugador actual puede ganar con una jugada, la hace
        for c in valid:
            if self._is_winning_move(board, c, p_turn):
                return c

        # 2. Si el oponente puede ganar en su siguiente jugada, se bloquea
        for c in valid:
            if self._is_winning_move(board, c, opp):
                return c

        # 3. Se filtran jugadas peligrosas (que permitan que el oponente gane en su siguiente turno)
        safe = []
        for c in valid:
            nb = self._drop(board, c, p_turn)
            if not any(self._is_winning_move(nb, oc, opp) for oc in self._valid_cols(nb)):
                safe.append(c)
        candidates = safe if safe else valid

        # 4. Se usa Minimax con poda alfa-beta para evaluar cada jugada candidata
        best_score = -float("inf")
        best_cols = []
        alpha, beta = -float("inf"), float("inf")
        for c in candidates:
            nb = self._drop(board, c, p_turn)
            score = self._min_value(nb, self.depth - 1, alpha, beta, p_turn, opp)
            if score > best_score:
                best_score = score
                best_cols = [c]
                alpha = max(alpha, score)
            elif score == best_score:
                best_cols.append(c)

        # Se desempata eligiendo la jugada más cercana al centro
        center = COLS // 2
        best_cols.sort(key=lambda x: abs(x - center))
        return best_cols[0]

    # Parte "Max" del algoritmo Minimax (jugador actual)
    def _max_value(self, b, d, alpha, beta, me, opp):
        if self._has_four(b, me):
            return 10000 + d  # Gana cuanto antes mejor
        if self._has_four(b, opp):
            return -10000 - d  # El rival gana (muy mal)
        if d == 0:
            return self._eval(b, me)  # Límite de profundidad: se evalúa heurísticamente

        v = -float("inf")
        for c in self._valid_cols(b):
            nb = self._drop(b, c, me)
            v = max(v, self._min_value(nb, d - 1, alpha, beta, me, opp))
            if v >= beta:
                return v  # Poda beta
            alpha = max(alpha, v)
        return v if v != -float("inf") else self._eval(b, me)

    # Parte "Min" del algoritmo Minimax (turno del oponente)
    def _min_value(self, b, d, alpha, beta, me, opp):
        if self._has_four(b, me):
            return 10000 + d
        if self._has_four(b, opp):
            return -10000 - d
        if d == 0:
            return self._eval(b, me)

        v = float("inf")
        for c in self._valid_cols(b):
            nb = self._drop(b, c, opp)
            v = min(v, self._max_value(nb, d - 1, alpha, beta, me, opp))
            if v <= alpha:
                return v  # Poda alfa
            beta = min(beta, v)
        return v if v != float("inf") else self._eval(b, me)

    # Devuelve las columnas válidas donde se puede colocar una ficha
    def _valid_cols(self, b):
        return [c for c in range(COLS) if b[0, c] == EMPTY]

    # Simula una jugada en una copia del tablero, dejando caer la ficha en la columna col
    def _drop(self, b, col, player):
        nb = b.copy()
        for r in range(ROWS - 1, -1, -1):  # desde la fila inferior hacia arriba
            if nb[r, col] == EMPTY:
                nb[r, col] = player
                return nb
        return nb  # Fallback

    # Evalúa si jugar en col da una victoria inmediata
    def _is_winning_move(self, b, col, player):
        if b[0, col] != EMPTY:
            return False
        nb = self._drop(b, col, player)
        return self._has_four(nb, player)

    # Revisa si el jugador tiene 4 en línea (horizontal, vertical o diagonal)
    def _has_four(self, b, player):
        for r in range(ROWS):
            for c in range(COLS - 3):
                if np.all(b[r, c:c+4] == player):
                    return True
        for c in range(COLS):
            for r in range(ROWS - 3):
                if np.all(b[r:r+4, c] == player):
                    return True
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(b[r+i, c+i] == player for i in range(4)):
                    return True
        for r in range(ROWS - 3):
            for c in range(3, COLS):
                if all(b[r+i, c-i] == player for i in range(4)):
                    return True
        return False

    # Heurística de evaluación del tablero
    def _eval(self, b, me):
        opp = -me
        score = 0

        # Bonificación por controlar el centro
        center_col = b[:, COLS // 2]
        score += 3 * np.count_nonzero(center_col == me)
        score -= 3 * np.count_nonzero(center_col == opp)

        # Función auxiliar para evaluar una ventana de 4 posiciones
        def wscore(window):
            myc = np.count_nonzero(window == me)
            opc = np.count_nonzero(window == opp)
            emp = np.count_nonzero(window == EMPTY)
            if myc > 0 and opc > 0:
                return 0  # ventana bloqueada
            if myc == 3 and emp == 1:
                return 100
            if myc == 2 and emp == 2:
                return 10
            if myc == 1 and emp == 3:
                return 1
            if opc == 3 and emp == 1:
                return -80
            if opc == 2 and emp == 2:
                return -8
            return 0

        # Recorre todo el tablero sumando el puntaje de cada ventana
        for r in range(ROWS):
            for c in range(COLS - 3):
                score += wscore(b[r, c:c+4])
        for c in range(COLS):
            for r in range(ROWS - 3):
                score += wscore(b[r:r+4, c])
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                score += wscore(np.array([b[r+i, c+i] for i in range(4)]))
        for r in range(ROWS - 3):
            for c in range(3, COLS):
                score += wscore(np.array([b[r+i, c-i] for i in range(4)]))
        return score

MyPolicy = UCB1Agent

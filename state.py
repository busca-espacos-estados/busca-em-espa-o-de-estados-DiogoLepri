from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos válidos a partir deste estado.

        Cada filho corresponde a deslizar uma peça para o espaço vazio, ou seja,
        a mover o ESPAÇO VAZIO em uma das quatro direções (quando não sai do
        tabuleiro 3x3). O `cost` de cada filho é `self.cost + 1`.
        """
        i = self.blank_index           # índice plano (0..8) do espaço vazio
        row, col = divmod(i, 3)        # linha e coluna correspondentes

        # Movimento do ESPAÇO VAZIO -> deslocamento (dlinha, dcoluna)
        moves = {
            "UP":    (-1, 0),
            "DOWN":  (1, 0),
            "LEFT":  (0, -1),
            "RIGHT": (0, 1),
        }

        children: List["State"] = []
        for action, (dr, dc) in moves.items():
            nr, nc = row + dr, col + dc
            if 0 <= nr < 3 and 0 <= nc < 3:        # continua dentro do tabuleiro
                j = nr * 3 + nc                    # índice plano do destino
                tiles = list(self.tiles)
                tiles[i], tiles[j] = tiles[j], tiles[i]   # troca vazio <-> peça
                children.append(
                    State(tuple(tiles), parent=self, action=action, cost=self.cost + 1)
                )
        return children

    def path(self) -> List["State"]:
        """Retorna a sequência de estados do estado inicial até este.

        Sobe pelos ponteiros `parent` até a raiz e inverte a ordem.
        """
        sequence: List["State"] = []
        node: Optional["State"] = self
        while node is not None:
            sequence.append(node)
            node = node.parent
        sequence.reverse()
        return sequence

    def actions(self) -> List[str]:
        """Retorna a sequência de ações do estado inicial até este.

        Reaproveita path(): cada estado (exceto o inicial) guarda em `action`
        o movimento que o gerou.
        """
        return [state.action for state in self.path() if state.action is not None]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")

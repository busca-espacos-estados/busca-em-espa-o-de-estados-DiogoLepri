import heapq
import itertools
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):
    """Busca A* — ordena a fronteira por f(n) = g(n) + h(n).

    g(n) = custo do caminho até n (state.cost); h(n) = heurística.
    Heurística: distância de Manhattan, que é admissível (nunca superestima,
    pois cada movimento desloca uma peça em apenas uma casa) e consistente,
    logo o A* é ótimo e basta testar o objetivo ao retirar o nó da fronteira.
    """

    def heuristic(self, state: State) -> int:
        """Soma das distâncias de Manhattan de cada peça até sua posição final.

        No objetivo (1, 2, ..., 8, 0), a peça de valor v fica no índice v - 1.
        A peça 0 (espaço vazio) é ignorada.
        """
        distance = 0
        for index, value in enumerate(state.tiles):
            if value != 0:
                row, col = divmod(index, 3)
                goal_row, goal_col = divmod(value - 1, 3)
                distance += abs(row - goal_row) + abs(col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        counter = itertools.count()    # desempate estável entre f(n) iguais
        # Fronteira: heap de (f, contador, estado).
        frontier = [(initial.cost + self.heuristic(initial), next(counter), initial)]
        # Melhor g(n) conhecido para cada estado.
        best_g = {initial: initial.cost}

        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            _, _, node = heapq.heappop(frontier)

            # Entrada obsoleta: já achamos um caminho melhor para este estado.
            if node.cost > best_g.get(node, float("inf")):
                continue

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=node.cost,
                )

            nodes_expanded += 1

            for child in node.neighbors():
                g = child.cost
                if g < best_g.get(child, float("inf")):
                    best_g[child] = g
                    nodes_generated += 1
                    heapq.heappush(
                        frontier,
                        (g + self.heuristic(child), next(counter), child),
                    )

            if len(frontier) > max_frontier_size:
                max_frontier_size = len(frontier)

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0,
        )

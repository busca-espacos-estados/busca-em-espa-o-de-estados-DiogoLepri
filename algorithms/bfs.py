from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):
    """Busca em Largura (FIFO).

    Com custo de passo uniforme (= 1), a BFS é completa e ótima: a primeira vez
    que alcança o objetivo encontra o caminho de menor número de movimentos.
    Usa busca em grafo (conjunto de estados já alcançados) para não reexpandir
    estados repetidos; o teste de objetivo é feito na geração de cada filho.
    """

    def search(self, initial: State) -> SearchResult:
        # Caso trivial: o estado inicial já é o objetivo.
        if initial.is_goal:
            return SearchResult(
                solution=initial,
                nodes_expanded=0,
                nodes_generated=1,
                max_frontier_size=1,
                depth=0,
            )

        frontier = deque([initial])     # fila FIFO
        reached = {initial}             # estados já gerados

        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            node = frontier.popleft()
            nodes_expanded += 1

            for child in node.neighbors():
                if child not in reached:
                    nodes_generated += 1
                    if child.is_goal:
                        return SearchResult(
                            solution=child,
                            nodes_expanded=nodes_expanded,
                            nodes_generated=nodes_generated,
                            max_frontier_size=max_frontier_size,
                            depth=child.cost,
                        )
                    reached.add(child)
                    frontier.append(child)

            if len(frontier) > max_frontier_size:
                max_frontier_size = len(frontier)

        # Fronteira esvaziou sem encontrar o objetivo (estado insolúvel).
        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0,
        )

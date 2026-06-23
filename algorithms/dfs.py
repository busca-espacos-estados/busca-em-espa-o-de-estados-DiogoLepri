from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):
    """Busca em Profundidade limitada (LIFO).

    Explora um ramo o mais fundo possível antes de retroceder, usando uma pilha.
    O `depth_limit` evita o aprofundamento infinito e poda ramos cujo custo
    ultrapassa o limite. Mantém um conjunto de estados visitados para evitar
    ciclos. NÃO é ótima: o caminho encontrado costuma ser bem mais longo que o
    do BFS/A*.
    """

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        stack = [initial]          # pilha LIFO
        reached = {initial}        # estados já colocados na pilha

        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while stack:
            node = stack.pop()

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=node.cost,
                )

            nodes_expanded += 1

            # Só expande enquanto não atingiu o limite de profundidade.
            if node.cost >= self.depth_limit:
                continue

            # `reversed` mantém a ordem UP/DOWN/LEFT/RIGHT ao desempilhar.
            for child in reversed(node.neighbors()):
                if child not in reached:
                    reached.add(child)
                    nodes_generated += 1
                    stack.append(child)

            if len(stack) > max_frontier_size:
                max_frontier_size = len(stack)

        # Pilha esvaziou sem encontrar o objetivo dentro do limite.
        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
            depth=0,
        )

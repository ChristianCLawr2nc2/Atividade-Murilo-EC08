import heapq
import sys

NULO = None  # aqui o nulo não será preenchido na tabela como 0, para não confundir com arestas de peso 0
INF = float("inf")


class Grafo:

    # grafo representado por matriz de adjacência
    def __init__(self, n):
        self.n = n
        self.M = [[NULO] * n for _ in range(n)]

    # adiciona aresta (i,j) com peso w
    def add_aresta(self, i, j, w):
        if w is None or w < 0:
            raise ValueError(f"Peso invalido em ({i},{j}): {w}")
        self.M[i][j] = w
        self.M[j][i] = w  # simetria

    # retorna lista de tuplas (v, w) com vizinhos v de u e peso w da aresta (u,v)
    def vizinhos(self, u):
        return [(v, self.M[u][v]) for v in range(self.n) if self.M[u][v] is not NULO]

    # imprime a matriz de adjacência
    def imprimir(self):
        print("      " + "".join(f"S{j:<4}" for j in range(self.n)))
        for i in range(self.n):
            print(f"S{i}  | " + "".join(
                f"{('--' if x is NULO else x):<5}" for x in self.M[i]))


# Função que gera os pesos das arestas do grafo
def pesos_ra(ra):
    d1, d2, d3, d4, d5, d6 = [int(c) for c in ra]
    arestas = [
        (0, 1, 10 + (d6 % 5)),            # e1
        (0, 2, 15 + (d5 % 7)),            # e2
        (1, 2, 8 + (d4 % 4)),             # e3
        (1, 3, 12 + (d3 % 6)),            # e4
        (2, 4, 14 + (d2 % 5)),            # e5
        (2, 5, 9 + (d1 % 6)),             # e6
        (3, 4, 7 + ((d5 + d6) % 5)),      # e7
        (3, 6, 11 + ((d4 + d5) % 6)),     # e8
        (4, 5, 6 + ((d3 + d4) % 4)),      # e9
        (4, 7, 16 + ((d2 + d3) % 7)),     # e10
        (5, 7, 18 + ((d1 + d2) % 8)),     # e11
        (6, 7, 9 + ((d5 + d1) % 5)),      # e12
        (1, 4, 20 + (d6 % 4)),            # e13
    ]
    destino = 7 if d6 % 2 == 0 else 6
    return arestas, destino

# Algoritmo de Dijkstra para encontrar o caminho mais curto em um grafo ponderado
def dijkstra(g, origem, destino=None, trace=False):
    L = [INF] * g.n
    ant = [None] * g.n
    fechado = [False] * g.n
    L[origem] = 0
    ordem = []
    for it in range(1, g.n + 1):
        # desempate: menor L, depois menor indice
        u = min((v for v in range(g.n) if not fechado[v] and L[v] < INF),
                key=lambda v: (L[v], v), default=None)
        if u is None:
            break
        fechado[u] = True
        ordem.append(u)
        atualizados = []
        for v, w in g.vizinhos(u):
            if not fechado[v] and L[u] + w < L[v]:
                L[v] = L[u] + w
                ant[v] = u
                atualizados.append(f"Ant[S{v}]=S{u} ({L[u]}+{w}={L[v]})")
        if trace:
            cols = [f"[{L[v]}]" if fechado[v] else ("inf" if L[v] == INF else str(L[v]))
                    for v in range(g.n)]
            print(f"{it:>2} | S{u} | {L[u]:>3} | " + " ".join(f"{c:>5}" for c in cols)
                  + " | " + "; ".join(atualizados))
        if destino is not None and u == destino:
            break
    return L, ant, ordem

# Função que reconstrói o caminho mais curto a partir do vetor de antecessores
def caminho(ant, origem, destino):
    rota, v = [], destino
    while v is not None:
        rota.append(v)
        v = ant[v]
    rota.reverse()
    return rota if rota and rota[0] == origem else []

# Algoritmo de Prim para encontrar a árvore geradora mínima de um grafo ponderado
def prim(g, origem=0):
    visitado = [False] * g.n
    pq = [(0, origem, None)]
    arestas, total = [], 0
    while pq:
        w, u, pai = heapq.heappop(pq)
        if visitado[u]:
            continue
        visitado[u] = True
        total += w
        if pai is not None:
            arestas.append((pai, u, w))
        for v, wv in g.vizinhos(u):
            if not visitado[v]:
                heapq.heappush(pq, (wv, v, u))
    return total, arestas


def fmt_rota(r):
    return " -> ".join(f"S{v}" for v in r)




if __name__ == "__main__":
    RA = sys.argv[1] if len(sys.argv) > 1 else "250107"
    arestas, destino = pesos_ra(RA)
    g = Grafo(8)
    for i, (a, b, w) in enumerate(arestas, 1):
        g.add_aresta(a, b, w)
        print(f"e{i:<2} (S{a},S{b}) = {w} km")
    print(f"\nRA={RA}  destino=S{destino}\n")


    # nesse trecho o grafo é impresso e o algoritmo de Dijkstra é executado a partir do nó S0, com rastreamento detalhado das iterações.
    print("Matriz de adjacencia 8x8 (-- = NULO):")
    g.imprimir()

    # Executa Dijkstra a partir de S0
    print("\nTeste de mesa (Dijkstra a partir de S0):")
    print("It | u  | L[u] | " + " ".join(f"{'L[S'+str(v)+']':>5}" for v in range(8)) + " | Antecessores")
    L, ant, ordem = dijkstra(g, 0, destino, trace=True)
    print(f"\nCusto minimo S0 -> S{destino}: {L[destino]} km")
    print("Rota otima:", fmt_rota(caminho(ant, 0, destino)))
    print("Ordem de fechamento:", ", ".join(f"S{v}" for v in ordem))
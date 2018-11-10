import random

class Graph(object):
    def __init__(self, distance: list, rank: int):
        self.matrix = distance
        self.rank = rank
        self.pheromone = [[1 for j in range(rank)] for i in range(rank)]


class ACO(object):
    def __init__(self, ant_count: int, alpha: float, beta: float, rho: float):
        self.rho = rho
        self.beta = beta
        self.alpha = alpha
        self.ant_count = ant_count

    def _update_pheromone(self, graph: Graph, ants: list):
        for i, row in enumerate(graph.pheromone):
            for j, col in enumerate(row):
                graph.pheromone[i][j] *= (1-self.rho)
                for ant in ants:
                    graph.pheromone[i][j] += ant.pheromone_delta[i][j]

    def solve(self, graph: Graph):
        best_cost = float('inf')
        best_solution = []
        ants = [_Ant(self, graph) for i in range(self.ant_count)]
        for ant in ants:
            for __ in range(graph.rank - 1):
                ant._select_next()
            ant.total_cost += graph.matrix[ant.tabu[-1]][ant.tabu[0]]
            if ant.total_cost < best_cost:
                best_cost = ant.total_cost
                best_solution = [] + ant.tabu
            ant._update_pheromone_delta()
        self._update_pheromone(graph, ants)
        # print('generation #{}, best cost: {}, path: {}'.format(gen, best_cost, best_solution))
        return best_solution, best_cost


class _Ant(object):
    def __init__(self, aco: ACO, graph: Graph):
        self.colony = aco
        self.graph = graph
        self.total_cost = 0.0
        self.tabu = []  # ant temp path
        self.pheromone_delta = []  # the local increase of pheromone
        self.allowed = [i for i in range(graph.rank)]  # nodes which are allowed for the next selection
        self.eta = [[0 if i == j else 1 / graph.matrix[i][j] for j in range(graph.rank)] for i in range(graph.rank)]  # heuristic information
        start = random.randint(0, graph.rank - 1)  # generate randon integer between (0,rank-1)
        self.tabu.append(start)
        self.current = start
        self.allowed.remove(start)

    def _select_next(self):
        denominator = 0
        #cum_prob = []
        for i in self.allowed:
            denominator += self.graph.pheromone[self.current][i] ** self.colony.alpha * self.eta[self.current][i] ** self.colony.beta
        probabilities = [0 for i in range(self.graph.rank)]  # probabilities for moving to a node in the next step
        for i in range(self.graph.rank):
            try:
                self.allowed.index(i)  # test if allowed list contains i
                probabilities[i] = self.graph.pheromone[self.current][i] ** self.colony.alpha * self.eta[self.current][i] ** self.colony.beta / denominator
                #cum_prob.append(probabilities[i])
            except ValueError: # due to infity
                pass  # do nothing
        selected = 0
        fg = 1
        while fg == 1:
            rand = random.uniform(0, 1)
            for i, probability in enumerate(probabilities):
                if probability > rand:
                    selected = i
                    fg = 0
                    break
        self.allowed.remove(selected)
        self.tabu.append(selected)
        self.total_cost += self.graph.matrix[self.current][selected]
        self.current = selected

    def _update_pheromone_delta(self):
        self.pheromone_delta = [[0 for j in range(self.graph.rank)] for i in range(self.graph.rank)]
        for k in range(1, len(self.tabu)):
            i = self.tabu[k - 1]
            j = self.tabu[k]
            self.pheromone_delta[i][j] = 1 / self.total_cost

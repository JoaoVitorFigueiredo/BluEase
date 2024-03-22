# nó é para wayfind
# ponto representa o utilizador
import networkx as nx


class Node:
    def __init__(self, pos, connection=None, heuristic=0):
        self.__connection = connection
        self.__beacon = None
        self.__heuristic = heuristic  # ?
        self.__visit_order = None
        self.__pos = pos

    def get_connection(self):
        return self.__connection

    def add_beacon(self, beacon):
        self.__beacon = beacon

    def get_beacon(self):
        return self.__beacon

    def get_pos(self):
        return self.__pos


class Graph:
    def __init__(self, nodes=None):
        self.__nx_graph = nx.DiGraph()

        if nodes is not None:
            self.__nodes = Graph.convert_to_dict(nodes)

    def set_nodes(self, nodes):
        self.__nodes = nodes

    def get_nodes(self):
        return self.__nodes

    def wayfind(self,start_node,end_node):
        """
        open -> caminhos já vistos
        closed -> lista dos nós caminho final
        """

        open = {}
        found_path = []
        open[tuple([0, start_node])] = 0

        while open != {}:
            if len(open) == 1:
                cheapest_path = list(open.keys())[0]
            else:
                temp_cost = -1
                for i in range(len(open)):  # Encontrarmo caminho mais curto de todos os caminhos do open
                    path = list(open.keys())[i]
                    path_cost = open[path]
                    if temp_cost == -1:
                        temp_cost = path_cost
                        cheapest_path = path
                    elif path_cost < temp_cost:
                        temp_cost = path_cost
                        cheapest_path = path

            print(cheapest_path)
            print(type(cheapest_path))
            print(cheapest_path[-1])

            # cheapest_path[-1] -> ultimo nó visitado
            if cheapest_path[-1] == end_node:
                for i in range(1, len(cheapest_path) - 1):
                    found_path.append(cheapest_path[i])
                return found_path

            for neighbor in self.__get_neighbors(cheapest_path[-1]):
                neighbor_path_cost = 0
                for i in range(1, len(cheapest_path) - 1):
                    neighbor_path_cost += self.__get_cost(cheapest_path[i], cheapest_path[i + 1])
                neighbor_path_cost += (self.__get_cost(cheapest_path[-1], neighbor))
                temp_tuple = cheapest_path + tuple([neighbor])
                open[temp_tuple] = neighbor_path_cost
            del open[cheapest_path]
        return []

    def __get_neighbors(self, node):
        return list(self.__nx_graph.neighbors(node))

    def __get_cost(self, node1, node2):
        return self.__nx_graph[node1][node2]["weight"]

    @staticmethod
    def convert_to_dict(nodes):
        new_graph = {}
        for connection in nodes:
            if connection[0] in new_graph.keys():
                new_graph[connection[0]].append([connection[1], connection[2]])
            elif connection[1] in new_graph.keys():
                new_graph[connection[1]].append([connection[0], connection[2]])
            else:
                new_graph[connection[0]] = [[connection[1], connection[2]]]
        return new_graph


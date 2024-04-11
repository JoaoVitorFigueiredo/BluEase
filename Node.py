# nó é para wayfind
# ponto representa o utilizador
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




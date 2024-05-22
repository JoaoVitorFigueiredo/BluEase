from Node import Node
from mysql import connector
from Building import Building
from Spot import Spot
from InterestPoint import InterestPoint
import networkx as nx

class BluEase:
    def __init__(self):
        # Alterar estas informações para funcionar
        self.get_info()
        print("rodou o init")

        # receber informações
        # guardá-las da melhor maneira
        self.__beacons = []
        # hashmap de key beacon, conteúdo lista de nós(?)
        self.__userX = 0
        self.__userY = 0
        self.__beacon_path = []


    def set_beacon_path(self, node_path):
        self.__beacon_path = []
        for node in node_path:
            self.__beacon_path.append(node.get_beacon())

    def get_beacon_path(self):
        return self.__beacon_path

    def get_building(self):
        return self.building

    def get_location_range(self, beacon):
        return  # Lista de beacons do nó atual

    def get_chosen_room(self, room_name):
        return self.__spots[room_name]

    def reset_beacon_path(self):
        self.__beacon_path = []

    def wayfind(self, start_node, end_node):  # Pedir socorro ao João
        found_path = []
        open, closed = {}, []
        open[tuple([0, start_node])] = 0
        closed.append(start_node)
        while open != []:
            if len(open) == 1:
                cheapest_path = list(open.keys())[0]
            else:
                temp_cost = -1
                for i in range(len(open)):
                    path = list(open.keys())[i]
                    path_cost = open[path]
                    if temp_cost == -1:
                        temp_cost = path_cost
                        cheapest_path = path
                    elif path_cost < temp_cost:
                        temp_cost = path_cost
                        cheapest_path = path
            if cheapest_path[-1] == end_node:
                for i in range(1, len(cheapest_path) - 1):
                    found_path.append(cheapest_path[i])
                found_path.append(end_node)
                return found_path
                #return ["1","2","3","6","11","10","9","10","11","12","7","8","7","4","5","4","7","12","16","15","13","15","16","17","14","17","18","19","18","25","26","25","21","16","20","21","17","21","18","21","20","17","20","23","22","23","27","23","24","23","21"]
            closed.append(cheapest_path[-1])
            for neighbor in list(self.__graph.neighbors(cheapest_path[-1])):
                # for neighbor in self.graph.get_neighbors(cheapest_path[-1]):
                neighbor_path_cost = 0
                for i in range(1, len(cheapest_path) - 1):
                    neighbor_path_cost += self.__graph[cheapest_path[i]][cheapest_path[i + 1]]['weight']
                    # neighbor_path_cost += self.graph.get_cost(cheapest_path[i], cheapest_path[i+1])
                neighbor_path_cost += self.__graph[cheapest_path[-1]][neighbor]['weight']
                # neighbor_path_cost+=(self.graph.get_cost(cheapest_path[-1], neighbor)+neighbor.heuristic)
                temp_tuple = cheapest_path + tuple([neighbor])
                open[temp_tuple] = neighbor_path_cost
            del open[cheapest_path]
        return closed, []
    # algoritmo A*
    

    # retorna uma lista de nós
    def get_nodes(self):
        return self.__nodes

    def get_edges(self):
        return self.__edges

    def get_info(self):
        hostname = "v1u.h.filess.io"
        database = "bluease_tinycitymy"
        port = "3307"
        username = "bluease_tinycitymy"
        password = "1ebb0a74b1fa3d4df3887283e8b8cca43d0ff43b"


        connection = connector.connect(host=hostname, database=database, user=username, password=password,
                                                 port=port)
        if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
        else:
            print("Erro na conexão")

        cursor.execute("select numero_edificio, nome, codigo_cliente from edificio where nome = 'Iscte-Sintra'")

        active_building_info = cursor.fetchone()

        active_building_id = active_building_info[0]

        self.building = Building(active_building_info[2], active_building_info[1])

        cursor.execute(
            f"select nome, coordenadas, piso, tamanho_espaço, ponto, numero_espaço from espaço where numero_edificio = {active_building_id}"
        )

        for name, coordinates, floor, spot_type, ponto, spot_id in cursor.fetchall():

            coordinates = coordinates.replace("(", "")
            coordinates = coordinates.replace(")", "")
            coordinates = coordinates.split(",")

            new_spot = Spot(name, int(coordinates[0]), int(coordinates[1]), int(floor), spot_type, ponto)

            cursor.execute(
                f"select coordenadas, descrição, tipo_espaço, ponto from ponto_de_interesse where numero_espaço={spot_id}"
            )

            for ip_coordinates, description, ip_type, ponto in cursor.fetchall():
                ip_coordinates = ip_coordinates.replace("(", "")
                ip_coordinates = ip_coordinates.replace(")", "")
                ip_coordinates = ip_coordinates.split(",")

                new_spot.getInterest_points().append(
                    InterestPoint.new_InterestPoint(int(ip_coordinates[0]), int(ip_coordinates[1]), description, ponto, ip_type))

            self.building.get_spots().append(new_spot)

        cursor.execute(
            f"select coordenadas, numero_ponto from ponto where numero_edificio = {active_building_id}"
        )

        self.__nodes = {}
        self.__edges = []

        for coordenadas in cursor.fetchall():
            ip_coordinates = coordenadas[0].replace("(", "")
            ip_coordinates = ip_coordinates.replace(")", "")
            ip_coordinates = ip_coordinates.split(",")
            self.__nodes[f'{coordenadas[1]}'] = (ip_coordinates[0], ip_coordinates[1])
            cursor.execute(f"select ponto_1, ponto_2, custo from aresta where ponto_1 = {coordenadas[1]}")
            for aresta in cursor.fetchall():
                self.__edges.append([str(aresta[0]), str(aresta[1]), aresta[2]])

        print(self.__nodes)
        print(self.__edges)

        self.__graph = nx.Graph()
        for i in self.__nodes.keys():
            self.__graph.add_node(i, pos=(self.__nodes[i]))
        for i in range(len(self.__edges)):
            self.__graph.add_edge(self.__edges[i][0], self.__edges[i][1], weight=self.__edges[i][2])

        connection.close()


if __name__ == "__main__":
    """"
    be = BluEase()

    building = be.get_building()
    print(building.name)
    spots = building.get_spots()
    for spot in spots:
        print("--------------------")
        print(spot.get_name())
        for interest_point in spot.getInterest_points():
            print(interest_point.getType())
        print("--------------------")
    """
    database = connector.connect(user="root", password="qwer",
                                 host="localhost", database="bluease")

    cursor = database.cursor()

    coord = "(100,100)"

    cursor.execute(f'insert into ponto () values (2,1,1,{coord})')


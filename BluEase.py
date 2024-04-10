from Graph import Graph, Node
from mysql import connector
from Building import Building
from Spot import Spot
from InterestPoint import InterestPoint



class BluEase:
    def __init__(self):
        # Alterar estas informações para funcionar
        database = connector.connect(user="root",password="qwer",
                           host="localhost", database="bluease")

        cursor = database.cursor()

        cursor.execute("select numero_edificio, nome, codigo_cliente from edificio where nome = 'Iscte-Sintra'")

        active_building_info = cursor.fetchone()

        active_building_id = active_building_info[0]

        self.building = Building(active_building_info[2], active_building_info[1])

        cursor.execute(f"select nome, coordenadas, piso, tamanho_espaço, numero_espaço from espaço where numero_edificio = {active_building_id}")

        for name, coordinates, floor, spot_type, spot_id in cursor.fetchall():

            coordinates = coordinates.replace("(","")
            coordinates = coordinates.replace(")", "")
            coordinates = coordinates.split(",")

            new_spot = Spot(name, int(coordinates[0]), int(coordinates[1]), int(floor), spot_type)

            cursor.execute(f"select coordenadas, descrição, tipo_espaço from ponto_de_interesse where numero_espaço={spot_id}")
            for ip_coordinates, description, ip_type in cursor.fetchall():

                ip_coordinates = ip_coordinates.replace("(", "")
                ip_coordinates = ip_coordinates.replace(")", "")
                ip_coordinates = ip_coordinates.split(",")

                new_spot.getInterest_points().append(InterestPoint.new_InterestPoint(int(ip_coordinates[0]),int(ip_coordinates[1]),description,ip_type))

            self.building.get_spots().append(new_spot)

        cursor.execute(f"select coordenadas, numero_ponto from ponto where numero_edificio = {active_building_id}")

        self.__nodes = []
        self.__coordinates = []
        self.__connections = []

        for coordenadas in cursor.fetchall():
            ip_coordinates = coordenadas[0].replace("(", "")
            ip_coordinates = ip_coordinates.replace(")", "")
            ip_coordinates = ip_coordinates.split(",")
            new_dot = Node((ip_coordinates[0], ip_coordinates[1]))
            self.__nodes.append(new_dot)
            self.__coordinates.append([coordenadas[1],int(ip_coordinates[0]),int(ip_coordinates[1])])
            cursor.execute(f"select ponto_1, ponto_2, custo from aresta where ponto_1 = {coordenadas[1]}")
            for aresta in cursor.fetchall():
                self.__connections.append([aresta[0],aresta[1],aresta[2]])













        # receber informações
        # guardá-las da melhor maneira
        self.__beacons = []

        self.__spots = {}  # hashmap de key nome, conteúdo sala
         # hashmap de key beacon, conteúdo lista de nós(?)
        self.__userX = 0
        self.__userY = 0
        self.__graph = Graph()  # Pegar conjunto de nós no database
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
        return self.__graph.wayfind(start_node, end_node)
    # algoritmo A*
    

    # retorna uma lista de nós
    def get_nodes(self):
        return self.__nodes

    def get_connections(self):
        return self.__connections


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


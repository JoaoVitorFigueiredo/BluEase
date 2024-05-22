class Spot:
    def __init__(self, name, coord_x, coord_y,floor, spot_type, node):  # Recebe
        self.__name = name
        self.__interest_points = []
        self.__coord_x = coord_x
        self.__coord_y = coord_y
        self.__floor = floor
        self.__type = spot_type
        self.__node = node

# sla se é assim, já decido
    def get_name(self):
        return self.__name

    def getInterest_points(self):
        return self.__interest_points

    def getCoord_x_Pin(self):
        return self.__coord_x

    def getCoord_y_Pin(self):
        return self.__coord_y

    def addInterest_point(self, new_point):
        self.__interest_points.append(new_point)

    def set__name(self, new_name):
        self.__name = new_name

    def get_pos(self):
        return (self.__coord_x,self.__coord_y)

    def get_node(self):
        return self.__node

    def write_on_database(self, cursor, s_number, building):
        print(f'\n----{self.__name}-------')
        cursor.execute(f"call add_espaco('{self.__name}',{self.__floor},{s_number},'pequeno',{building},'({self.__coord_x},{self.__coord_y})')")
        ip_number = 1
        for interest_point in self.__interest_points:
            interest_point.write_on_database(cursor, s_number, ip_number)
            ip_number += 1

    def get_pictures(self):
        return f"pictures/{self.__name}.png"
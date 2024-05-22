class InterestPoint:
    def __init__(self, coord_x, coord_y, description, node):
        self.__coord_x = coord_x
        self.__coord_y = coord_y
        self.__description = description
        self.icon = None
        self.__node = node

    def getCoord_x(self):
        return self.__coord_x

    def getCoord_y(self):
        return self.__coord_y

    def get_pos(self):
        return (self.__coord_x, self.__coord_y)

    def get_description(self):
        if self.__description is None:
            return self.getType()
        return self.__description

    def getType(self):
        return None

    def get_icon(self):
        return self.icon

    def get_node(self):
        return self.__node

    def write_on_database(self, cursor, s_number, ip_number):
        print(self.getType())
        cursor.execute(f"call add_ponto_interesse('{self.getType()}','({self.__coord_x},{self.__coord_y})',{s_number}, '{self.get_description()}',{ip_number})")

    @staticmethod
    def new_InterestPoint(coord_x, coord_y, description, node, ip_type):
        if ip_type == "WC Homens":
            return (MaleBathroom(coord_x,coord_y,description, node))
        elif ip_type == "WC Mulheres":
            return (FemaleBathroom(coord_x,coord_y,description, node))
        elif ip_type == "Máquina de vendas":
            return (VendingMachine(coord_x,coord_y,description, node))
        elif ip_type == "Balcão de informação":
            return (InformationDesk(coord_x,coord_y,description, node))
        elif ip_type == "Elevador":
            return (Elevator(coord_x,coord_y,description, node))
        elif ip_type == "Escadas":
            return (Stairs(coord_x,coord_y,description, node))
        elif ip_type == "Administração":
            return (Administration(coord_x,coord_y,description, node))
        elif ip_type == "Cafetaria":
            return (Cafeteria(coord_x,coord_y,description, node))
        elif ip_type == "Apresentações":
            return (Lectures(coord_x,coord_y,description, node))
        else:
            return (InterestPoint(coord_x,coord_y,description, node))

class MaleBathroom(InterestPoint):
    def __init__(self, coord_x, coord_y, description, node):
        super().__init__(coord_x, coord_y, description, node)
        self.icon = 'icons/icons8-wc-man-100-2.png'

    def getType(self):
        return "WC Homens"


class FemaleBathroom(InterestPoint):
    def __init__(self, coord_x, coord_y, description, node):
        super().__init__(coord_x, coord_y, description, node)
        self.icon = 'icons/icons8-wc-woman-100-2.png'

    def getType(self):
        return "WC Mulheres"


class VendingMachine(InterestPoint):
    def __init__(self, coord_x, coord_y, description, node):
        super().__init__(coord_x, coord_y, description, node)
        self.icon = 'icons/icons8-vending-machine-100.png'

    def getType(self):
        return "Máquina de vendas"


class InformationDesk(InterestPoint):
    def __init__(self, coord_x, coord_y, description, node):
        super().__init__(coord_x,coord_y, description, node)
        self.icon = 'icons/icons8-reception-100.png'

    def getType(self):
        return "Balcão de informação"


class Elevator(InterestPoint):
    def __init__(self, coord_x, coord_y, description, node):
        super().__init__(coord_x,coord_y, description, node)
        self.icon = 'icons/icons quadrados/icons8-elevator-100-3.png'

    def getType(self):
        return "Elevador"


class Stairs(InterestPoint):
    def __init__(self, coord_x, coord_y, description, node):
        super().__init__(coord_x,coord_y, description, node)
        self.icon = 'icons/icons quadrados/icons8-stairs-100-5.png'

    def getType(self):
        return "Escadas"


class Administration(InterestPoint):
    def __init__(self, coord_x, coord_y, description, node):
        super().__init__(coord_x,coord_y, description, node)
        self.icon = 'icons/icons8-human-resources-100.png'

    def getType(self):
        return "Administração"


class Cafeteria(InterestPoint):
    def __init__(self, coord_x, coord_y, description, node):
        super().__init__(coord_x,coord_y, description, node)
        self.icon = 'icons/icons8-restaurant-100.png'

    def getType(self):
        return "Cafetaria"


class Lectures(InterestPoint):
    def __init__(self, coord_x, coord_y, description, node):
        super().__init__(coord_x,coord_y, description, node)
        self.icon = 'icons/icons8-projector-screen-100.png'

    def getType(self):
        return "Apresentações"
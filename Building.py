
class Building:
    def __init__(self, id_client, name):
        self.id_client = id_client
        self.name = name
        self.spots = []

    def get_number(self, cursor):
        cursor.execute(f"select numero_edificio from edificio as ed where ed.nome = '{self.name}';")
        return cursor.fetchone()[0]

    def get_spots(self):
        return self.spots

    def write_on_database(self, cursor, id):
        cursor.execute("start Transaction;")
        query = f"call add_edificio('{self.name}',{self.id_client},{id});"
        cursor.execute(query)
        number = 1

        for spot in self.spots:
            spot.write_on_database(cursor, number, id)
            number += 1

        cursor.execute("commit;")


if __name__ == "__main__":
    from mysql import connector
    from Spot import Spot
    from InterestPoint import *

    # Código para inserir as coisas na base de dados

    building = Building(102, "Iscte-Sintra")

    sc = connector.connect(user="root", password="qwer",
                           host="localhost", database="bluease")
    cursor = sc.cursor()

    building.spots.append(Spot("Receção",430,325,1,None))
    building.spots.append(Spot("Corredor lateral", 185, 320, 1, None))
    building.spots.append(Spot("Sala multiusos", 500, 750, 1, None))
    building.spots.append(Spot("UATA", 685, 600, 1, None))
    building.spots.append(Spot("Piso -1", 950, 630, 1, None))
    building.spots.append(Spot("Entrada", 430, 100, 1, None))
    building.spots.append(Spot("WC Homem - Copa", 260, 1060, 1, None))
    building.spots.append(Spot("WC Mulher - Área de serviço", 920, 1060, 1, None))


    building.spots[0].getInterest_points().append(InformationDesk(590,310,'Receção'))
    building.spots[1].getInterest_points().append(VendingMachine(193,100,'Máquina - comida/café'))
    building.spots[1].getInterest_points().append(Elevator(143,210,'Elevador'))
    building.spots[1].getInterest_points().append(Stairs(100,383,'Escadas - 2º andar'))
    building.spots[2].getInterest_points().append(Lectures(110,750,"Sala multiusos"))
    building.spots[2].getInterest_points().append(Stairs(100,505,'Escadas - estacionamento'))
    building.spots[3].getInterest_points().append(Administration(790,500,'UATA'))
    building.spots[4].getInterest_points().append(Stairs(1070,600,'Escadas - Piso -1'))
    building.spots[6].getInterest_points().append(MaleBathroom(125,1067,'WC Homens - 1ºAndar'))
    building.spots[6].getInterest_points().append(Cafeteria(365,1067,'Copa'))
    building.spots[7].getInterest_points().append(FemaleBathroom(1010,1067,'WC Mulheres - 1ºAndar'))


    building.write_on_database(cursor,1)

'''
        self.move = [('','Elevador',143,210,'icons/icons quadrados/icons8-elevator-100-3.png','icons/icons quadrados/icons8-elevator-100-4.png',''),
                  ('','Escadas - 2º andar',100,383,'icons/icons quadrados/icons8-stairs-100-5.png','icons/icons quadrados/icons8-stairs-100-6.png',''),
                  ('','Escadas - estacionamento',100,505,'icons/icons quadrados/icons8-stairs-100-5.png','icons/icons quadrados/icons8-stairs-100-6.png',''),
                  ('','Escadas - Piso -1',1070,600,'icons/icons quadrados/icons8-stairs-100-5.png','icons/icons quadrados/icons8-stairs-100-6.png','')]
        self.botoes = [('Receção''icons/icons8-reception-100.png','icons/icons8-reception-100-2.png','Receção.png'),
                  ('','Máquina - comida/café',193,100,'icons/icons8-vending-machine-100.png','icons/icons8-vending-machine-100-2.png',''),
                  ('','Sala multiusos',110,750,'icons/icons8-projector-screen-100.png','icons/icons8-projector-screen-100-2.png',''),
                  ('','WC Homens - 1ºAndar',125,1067,'icons/icons8-wc-man-100-2.png','icons/icons8-wc-man-100.png',''),
                  ('','WC Mulheres - 1ºAndar',1010,1067,'icons/icons8-wc-woman-100-2.png','icons/icons8-wc-woman-100.png',''),
                  ('UATA','UATA',790,500,'icons/icons8-human-resources-100.png','icons/icons8-human-resources-100-2.png',''),
                  ('','Copa',365,1067,'icons/icons8-restaurant-100.png','icons/icons8-restaurant-100-2.png','')]
'''


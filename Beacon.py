class Beacon:
    def __init__(self, id, room):  # antes do contrutor do beacon deve ser verificado o id inserido
        try:
            self.__id = int(id)
        except Exception:
            raise TypeError("id deve ser um número inteiro")

        self.__room = room


    def getId(self):
        return self.__id

    def getRoom(self):
        return self.__room

    def print_test(self):
        print('teste')


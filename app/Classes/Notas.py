class Nota:
    def __init__(self, nota, octava:int, rectangulo, figura="") -> None:
        self.nota = nota
        self.octava = octava
        self.rectangulo = rectangulo
        self.figura = figura
        self.pentagrama = None

    def set_pentagrama(self, pentagrama):
        self.pentagrama = pentagrama

class Partitura:
    def __init__(self, posiciones_pentagramas:list, notas:list, nombre:str) -> None:
        self.notas = notas
        self.posiciones_pentagramas = posiciones_pentagramas
        self.pentagramas = None
        self.nombre = nombre

        self.asignar_notas_a_pentagrama()

    def borrar_nota(self, index):
        self.notas = self.notas[:index] + self.notas[index + 1:]
        self.asignar_notas_a_pentagrama()

    def asignar_notas_a_pentagrama(self):
        index_pentagrama:int = 0
        index_notas:int = 0

        if not self.pentagramas:
            self.pentagramas = self.crear_lista_pentagramas()

        while index_pentagrama < len(self.posiciones_pentagramas):
            notas_pentagrama:list = []
            while index_notas < len(self.notas) and self.notas[index_notas].rectangulo[1] < self.posiciones_pentagramas[index_pentagrama][-1]:
                notas_pentagrama.append(self.notas[index_notas])
                index_notas += 1
            self.pentagramas[index_pentagrama].notas = notas_pentagrama
            self.pentagramas[index_pentagrama].asignar_pentagrama_a_nota()
            # lista_pentagramas.append(Pentagrama(notas_pentagrama, self.posiciones_pentagramas[index_pentagrama]))
            index_pentagrama += 1


    def crear_lista_pentagramas(self):
        return [Pentagrama([], posiciones) for posiciones in self.posiciones_pentagramas]


    def find_index_nota_at_position(self, pos):
        for i, nota in enumerate(self.notas):
            if pos[0] <= nota.rectangulo[3] and pos[0] >= nota.rectangulo[2] and pos[1] <= nota.rectangulo[1] and pos[1] >= nota.rectangulo[0]:
                return i

class Pentagrama:
    def __init__(self, notas, posiciones) -> None:
        self.notas = notas
        self.posiciones = posiciones
        self.asignar_pentagrama_a_nota()

    def asignar_pentagrama_a_nota(self):
        for nota in self.notas:
            nota.pentagrama = self
    
    def cambiar_nota(self, nota, atributo, valor):
        setattr(nota, atributo, valor)
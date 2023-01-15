class Nota:
    def __init__(self, nota:str, rectangulo:list, octava:int = 3, figura:str = "", alteracion:str = "Natural", numero_alteraciones:int = 1, alteracion_manual:bool = False) -> None:
        self.nota:str = nota
        self.octava:int = octava
        self.rectangulo:list = rectangulo
        self.figura:str = figura
        self.pentagrama:Pentagrama = None
        self.alteracion:str = alteracion
        self.numero_alteraciones:int = numero_alteraciones
        self.alteracion_manual:bool = alteracion_manual

    def set_pentagrama(self, pentagrama):
        self.pentagrama = pentagrama

class Partitura:
    def __init__(self, posiciones_pentagramas:list, notas:list, nombre:str, path_img_original:str, resized:bool, fraccion:float) -> None:
        self.notas = notas
        self.posiciones_pentagramas = posiciones_pentagramas
        self.pentagramas = None
        self.nombre = nombre
        self.path_img_original = path_img_original
        self.resized = resized
        self.fraccion = fraccion

        self.asignar_notas_a_pentagrama()

    def borrar_nota(self, index:int) -> None:
        """
        Elimina la nota de la lista de notas de la partitura y vuelve a asignar las notas a los pentagramas

        Args:
            index (int): El índice de la nota en la lista de notas de la partitura
        """
        self.notas = self.notas[:index] + self.notas[index + 1:]
        self.asignar_notas_a_pentagrama()

    def asignar_notas_a_pentagrama(self) -> None:
        """
            Asigna las notas pertenecientes a cada pentagrama a su pentagrama correspondiente
        """
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
            index_pentagrama += 1


    def crear_lista_pentagramas(self) -> list:
        """
        Crea una lista de pentagramas con las notas vacías
        """
        return [Pentagrama([], posiciones) for posiciones in self.posiciones_pentagramas]


    def find_index_nota_at_position(self, pos:list) -> int:
        """
        Encuentra el índice de la nota que se encuentra en la posicion dada

        Args:
            pos (list): La posicion

        Returns:
            (int): El índice de la nota, o None si no existe
        """
        for i, nota in enumerate(self.notas):
            if pos[0] <= nota.rectangulo[3] and pos[0] >= nota.rectangulo[2] and pos[1] <= nota.rectangulo[1] and pos[1] >= nota.rectangulo[0]:
                return i
        
        return None

class Pentagrama:
    def __init__(self, notas, posiciones) -> None:
        self.notas = notas
        self.posiciones = posiciones
        self.asignar_pentagrama_a_nota()

    def asignar_pentagrama_a_nota(self) -> None:
        """
        Asigna el pentagrama a cada nota de la lista de notas de este pentagrama
        """
        for nota in self.notas:
            nota.pentagrama = self
    
    def cambiar_nota(self, nota:Nota, atributo:str, valor) -> None:
        """
        Cambia el valor de un atributo de una nota

        Args:
            nota (Nota): La nota a la que cambiarle el valor del atributo
            atributo (str): El nombre del atributo a cambiar
            valor (Any): El nuevo valor
        """
        setattr(nota, atributo, valor)
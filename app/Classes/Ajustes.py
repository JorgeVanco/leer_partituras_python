class Ajustes:
    def __init__(self, UMBRAL_NEGRO: int = 200, FRACCION_MINIMA_PIXELES_NEGROS: float = 3/4, SIZE_PENTAGRAMA_IDEAL:int = 43):
        self.UMBRAL_NEGRO: int = UMBRAL_NEGRO  # considero negro cualquier valor menor que 140
        self.FRACCION_MINIMA_PIXELES_NEGROS: float = FRACCION_MINIMA_PIXELES_NEGROS
        self.SIZE_PENTAGRAMA_IDEAL:int = SIZE_PENTAGRAMA_IDEAL

from lectura_partituras.functions.functions import get_nombre_fichero, find_complete_path, sumar_desfase

COLOR_VERDE = "\033[1;32m"
COLOR_ROJO = "\033[1;31m"
COLOR_DEFECTO = "\033[0m"
GRIS = "\033[0;47m"
VERDE = "\033[1;42m"
DEFECTO = "\033[0m"
AMARILLO = "\033[0;43m"


def ok():
    print(f"{COLOR_VERDE}OK{COLOR_DEFECTO}")

def error():
    print(f"{COLOR_ROJO}ERROR{COLOR_DEFECTO}")

def test_get_nombre_fichero():
    print("- Función test_get_nombre_fichero(): ", end="")
    correct = "fichero.txt"
    path = "path/to/" + correct
    name = get_nombre_fichero(path)
    if name == correct:
        ok()
    else:
        error()
        print(f"\t{name} != {correct}")


def test_find_complete_path():
    print("- Función test_find_complete_path(): ", end="")

    file_path = __file__.replace("\\", "/")
    index = file_path.find("app")
    correct_path = file_path[:index]


    complete_path = find_complete_path(__file__)

    if complete_path == correct_path:
        ok()
    else:
        error()
        print(f"\t{complete_path} != {correct_path}")


def test_sumar_desfase():
    print("- Función test_sumar_desfase(): ", end="")
    desfase = 10
    posiciones = [0, 0, 0, 0]
    posiciones_nuevas = sumar_desfase(posiciones, desfase)

    if posiciones_nuevas == [desfase, desfase, 0, 0]:
        ok()
    else:
        error()


if __name__ == "__main__":
    test_get_nombre_fichero()
    test_find_complete_path()
    test_sumar_desfase()
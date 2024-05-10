import argparse


def imprimir_color(color):
    colores = {
        "rojo": "\033[91m",
        "verde": "\033[92m",
        "azul": "\033[94m",
        "amarillo": "\033[93m",
        "morado": "\033[95m",
        "cyan": "\033[96m",
        "blanco": "\033[97m",
    }
    if color in colores:
        print(colores[color] + "Este es el color " + color + "!" + "\033[0m")
    else:
        print("Color no válido")


def main():
    parser = argparse.ArgumentParser(
        description="Imprime un mensaje en el color especificado."
    )
    parser.add_argument(
        "-c",
        "--color",
        metavar="color",
        type=str,
        help="Especifica el color a imprimir",
    )
    args = parser.parse_args()
    if args.color:
        imprimir_color(args.color)


if __name__ == "__main__":
    main()

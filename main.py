
from celda import Celda
from niveles import Level
from tablero import Board


def main():

    while True :
        print("BUSCAMINAS")
        print("-"*10)
        print("1. Principiante (9x9, 10 minas")
        print("2. Intermedio (16x16, 40 minas")
        print("3. Experto (16x30, 99 minas")
        print("4. Leer fichero")
        print("5. Salir\n")

        choice = input("Escoja opcion: ").replace(" ", "")

        if choice == "1" :
            board = Board(level=Level.BEGINNER)
        elif choice == "2" :
            board = Board(level=Level.MEDIUM)
        elif choice == "3" :
            board = Board(level=Level.EXPERT)
        elif choice == "4" :
            fileName = input("Introduzca el nombre del fichero:")
            try:
                boardStr = readBoard(fileName)
                board = Board(boardLines=boardStr)
            except (OSError, IOError) :
                print("\n*** El fichero indicado no existe ***\n\n")
                continue 

        elif choice == "5" :
            exit()
        else :
            print("\n*** Opcion no valida ***\n\n")
            continue

        print(board)
        


def readBoard(fileName) :
    try :
        with open(fileName,"r") as f :
            boardStr = f.readlines()
    except :
        raise

    return boardStr


if __name__ == "__main__":
    main()

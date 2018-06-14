
from celda import Celda
from niveles import Level
from random import randint as rand

class Board :

    # Nombres de las filas y de las columnas
    ROWS_NAMES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&"
    COLS_NAMES = "abcdefghijklmnopqrstuvwxyz=+-:/"

    # Dimensiones de los tableros aleatorios

    DIMENSIONS = {'BEGINNER' : (9,9), 'MEDIUM' :(16,16),'EXPERT' : (30,16) }

    #Numero de minas de los tableros aleatorios
    MINES =  {'BEGINNER' : 10, 'MEDIUM' : 40,'EXPERT' : 99 }
    
    #---------------------------------------------------------------------------

    def __init__(self, boardLines = None, level = None):
       
        if boardLines != None :
            line1 = boardLines[0]
            rest = boardLines[1:]

            self._rows = line1[0]
            self._cols = line1[2]
            self._board = []

            for i in rest :
                row = []
                for j in i :
                    if j != '\n':
                        print(j,end=" ")                    
                        c = Celda(j)
                        row.append(c)
                print("")
                self._board.append(row)
        else :
            self._rows, self._cols = self.DIMENSIONS[level.name]
            self.board = level

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self) :
        return self._cols

    @property
    def board(self) :
        return self._board

    @board.setter
    def board(self,level) :
        rows,cols = self.DIMENSIONS[level.name]
        mines = self.MINES[level.name]
        self._board = []

        for i in range(0,rows) :
            row = []
            for j in range(0,cols) :
                a = rand(0,1)
                if a == 1 and mines > 0:
                    c = Celda('*')
                    mines -= 1
                else :
                    c = Celda('.')
                row.append(c)
            self._board.append(row)


    def __str__(self) :
        rowStr = []
        boardStr = []

        for i in self._board :            
            for j in i :
               rowStr.append(str(j))
               rowStr.append(" ")
            boardStr.append(''.join(rowStr))
            rowStr = []
        
        return "\n\n".join(boardStr)
            

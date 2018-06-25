
from celda import Celda
from niveles import Level
from random import randint as rand
import time

class Board :

    # Caracteres para dibujar cuadros
    COE = u'\u2500'  # ─
    CNS = u'\u2502'  # │
    CES = u'\u250C'  # ┌
    CSO = u'\u2510'  # ┐
    CNE = u'\u2514'  # └
    CON = u'\u2518'  # ┘
    COES = u'\u252C' # ┬
    CNES = u'\u251C' # ├
    CONS = u'\u2524' # ┤
    CONE = u'\u2534' # ┴
    
    # Nombres de las filas y de las columnas
    ROWS_NAMES = "ABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&"
    COLS_NAMES = "abcdefghijklmnopqrstuvwxyz=+-:/"

    # Dimensiones de los tableros aleatorios

    DIMENSIONS = {'BEGINNER' : (9,9), 'MEDIUM' :(16,16),'EXPERT' : (30,16) }

    #Numero de minas de los tableros aleatorios
    MINES =  {'BEGINNER' : 10, 'MEDIUM' : 40,'EXPERT' : 99 }
    
    # Posiciones de las celdas vecinas
    ODD_ROW_AROUND = [(0,-1),(0, 1),(-1,0),(1,0),(1,-1),(-1,-1)]
    EVEN_ROW_AROUND = [(0,-1),(0, 1),(-1,0),(1,0),(1,1),(-1,1)]

    #---------------------------------------------------------------------------

    def __init__(self, boardLines = None, level = None):
       
        if boardLines != None :
            line1 = boardLines[0].split(" ")
            rest = boardLines[1:]
            mines = 0
            self._rows = int(line1[0])
            self._cols = int(line1[1])
            self._board = []

            for i in rest :
                row = []
                for j in i :
                    if j != '\n':                
                        c = Celda(j)
                        row.append(c)
                        if c.mine :
                            mines += 1
                            
                self._board.append(row)
            
            self._minesLeft = mines
            
        else :
            self._rows, self._cols = self.DIMENSIONS[level.name]
            self._minesLeft = self.MINES[level.name]
            self.board = level

        self._minesMarked = 0
        self._initTime = time.process_time()
        self._elapsedTime = 0
        self.configureCells()

    def configureCells(self) :
        """ Asigna a cada celda sus celdas vecinas """
        for i,row in enumerate(self._board) :
            for j,cell in enumerate(row) :
                ls = []
                if i % 2 == 0:
                    positions = self.EVEN_ROW_AROUND
                else :
                    positions = self.ODD_ROW_AROUND

                for x,y in positions :
                    if i+x in range(0,self.rows) and  j+y in range(0,self.cols):
                            row2 = self._board[i+x]
                            ls.append(row2[j+y])

                cell.around = ls

    @property
    def rows(self):
        """ Obtine el número de filas del tablero """
        return self._rows

    @property
    def cols(self) :
        """ Obtiene el número de columnas del tablero """
        return self._cols

    @property
    def board(self) :
        """ Obtiene la matriz del tablero """
        return self._board

    @property
    def minesMarked(self) :
        """ Obtiene el número de minas marcadas """
        return self._minesMarked
    
    @property 
    def minesLeft(self) :
        """ Obtiene el número de minas sin marcar """
        return self._minesLeft
    
    @property
    def elapsedTime(self) :
        initTime = self._initTime
        self._initTime = time.process_time()
        self._elapsedTime = self._initTime - initTime + self._elapsedTime

        return self._elapsedTime


    @board.setter
    def board(self,level) :
        rows,cols = self.DIMENSIONS[level.name]
        mLeft = self.minesLeft
        self._board = []

        for i in range(0,rows) :
            row = []
            for j in range(0,cols) :
                a = rand(0,5)
                if a == 1 and mLeft > 0:
                    c = Celda('*')
                    mLeft -= 1
                else :
                    c = Celda('.')
                row.append(c)
            self._board.append(row)
        
        self._minesLeft -= mLeft

    def boardHead(self) : 
        """ Obtiene la cabecera del tablero donde se indica las minas sin marcar, 
            las minas marcadas y el tiempo transcurrido  """       
        head = "MINAS RESTANTES: {} | MARCADAS: {} | TIEMPO: {:.4f} seg.\n\n" 

        return head.format(self.minesLeft,self.minesMarked,self.elapsedTime) 
    
    def getCell(self, crow=None, ccol=None, coordinates=None) :
        """ Obtiene una celda dadas su fila y su columna en formato numérico 
            o dadas sus coordenadas en formato alfabético.   """
        if not coordinates :
            row = self._board[crow]
            c = row[ccol]
            return c
        else :
            rowIndex = self.ROWS_NAMES.index(coordinates[0])
            colIndex = self.COLS_NAMES.index(coordinates[1])

            row = self._board[rowIndex]
            c = row[colIndex]
            return c

    def rightFormat(self, movement) :
        """ Determina si un movimiento tiene un formato correcto """
        if (len(movement) != 3 or (movement[2] != '!' and movement[2] != '*') or 
            movement[0] not in self.ROWS_NAMES[:self.rows] or movement[1] not in self.COLS_NAMES[:self.cols]):
            return False
        return True
    
    def mark(self,cell) :
        """ Marca una celda no marcada o desmarcar una celda ya marcada. Para 
            poder marcar una celda debe estar cerrada y que el número de minas 
            que quedan por marcar sea mayor que cero"""

        c = self.getCell(coordinates=cell)
        if self.minesLeft == 0 :
            raise Exception("NO SE PUEDEN MARCAR MAS CELDAS QUE MINAS")
        if c.opened :
            raise Exception("NO SE PUEDE MARCAR UNA CELDA ABIERTA")
        
        c.marked = not c.marked
        self._minesLeft -= 1

    def open(self,cell) :
        c = self.getCell(coordinates=cell)  
        if c.marked :
            raise Exception("NO SE PUEDE ABRIR UNA CELDA MARCADA")       
        if not c.opened and c.n() > 0 :
            raise Exception("CELDA YA ABIERTA. NO SE PUEDEN ABRIR LAS CELDAS VECINAS POR NUMERO INSUFICIENTE DE MARCAS")       

    def move(self, mov) :
        """ Determina si un movimiento tiene un formato válido y realiza
            el marcado o la apertura de la celda correspondiente """
        if not self.rightFormat(mov) :
            raise Exception("ENTRADA ERRÓNEA")
        try :
            if mov[2] == "!" :
                self.mark(mov[:2])
            else :
                self.open(mov[:2])
        except Exception :
            raise

    def __str__(self) :
        rowStr = []
        boardStr = []
        row = 0     
        boardStr.append("   " + " ".join(self.COLS_NAMES[:self.cols]))
        for i in self._board :     
           
            if row%2 == 0 :
                rowStr.append(self.ROWS_NAMES[row] + " ")
            else :
                rowStr.append(self.ROWS_NAMES[row])
            col = 0
            for j in i :
               rowStr.append(str(j.n()))
               col += 1
            boardStr.append(' '.join(rowStr))
            rowStr = []
            row += 1
        
        return self.boardHead() + "\n\n".join(boardStr)
            

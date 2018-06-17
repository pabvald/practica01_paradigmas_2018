
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

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self) :
        return self._cols

    @property
    def board(self) :
        return self._board

    @property
    def minesMarked(self) :
       return self._minesMarked
    
    @property 
    def minesLeft(self) :
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
        head = "MINAS RESTANTES: {} | MARCADAS: {} | TIEMPO: {:.4f} seg.\n\n" 

        return head.format(self.minesLeft,self.minesMarked,self.elapsedTime) 
    
    def isMarked(self, row, col) :
        if row < 0 or row >= self.rows :
            return False
        if col < 0 or col >= self.cols :
            return False

        row = self._board[row]
        c = row[col]
        return c.marked
    
    def isMined(self, row, col) :
        if row < 0 or row >= self.rows :
            return False
        if col < 0 or col >= self.cols :
            return False
        
        row = self._board[row]
        c = row[col]
        return c.mine

    def n(self, row, col) :
        # n = número de celdas vecinas con mina – número de celdas vecinas marcadas
        mines = 0
        marked = 0
        defaultPositions = [(row,col-1),(row, col+1),(row-1,col),(row+1,col)]
        evenPositions = [(row+1,col+1),(row-1,col+1)]
        oddPositions = [(row+1,col-1),(row-1,col-1)]

        for x,y in defaultPositions :
            if self.isMarked(x,y) : marked += 1
            if self.isMined(x,y) : mines += 1              

        if row % 2 == 0:
            extraPositions = evenPositions
        else :
            extraPositions = oddPositions

        for x,y in extraPositions :
            if self.isMarked(x,y) : marked += 1
            if self.isMined(x,y) : mines += 1
           
        return mines - marked

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
               rowStr.append(str(self.n(row,col)))
               col += 1
            boardStr.append(' '.join(rowStr))
            rowStr = []
            row += 1
        
        return self.boardHead() + "\n\n".join(boardStr)
            

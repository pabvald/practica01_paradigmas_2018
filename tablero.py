
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
        """ Constructor."""
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
        self._initTime = time.perf_counter()
        self._ended = False
        self._won = False
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
    def ended(self) :
        """Determina si la partida ha finalizado(True) o no (False)"""
        if self._ended : 
            return True
        elif self.minesLeft > 0 :             
            return False
        else :
            self._won = True
            for row in self._board:
                for cell in row:
                    if  not cell.opened and not cell.marked :                         
                       self._won = False

            return self._won

    @property
    def won(self) :
        """ Determina si la partida ha sido ganada """
        return self._won

    @property
    def elapsedTime(self) :
        """ Obtiene el tiempo transcurrido desde que se creó el tablero """
        actualTime = time.perf_counter()
        return  actualTime - self._initTime


    @board.setter
    def board(self,level) :
        """ Configura el tablero de forma aleatoria añadiendo el número de
            minas correspondientes al nivel de dificultad """
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
            que quedan por marcar sea mayor que cero """

        c = self.getCell(coordinates=cell)

        if self.minesLeft == 0 :
            raise Exception("NO SE PUEDEN MARCAR MAS CELDAS QUE MINAS")
        if c.opened :
            raise Exception("NO SE PUEDE MARCAR UNA CELDA ABIERTA")
        
        if c.marked :
            c.marked = False
            self._minesLeft += 1
            self._minesMarked -= 1
        else :
            c.marked = True
            self._minesLeft -= 1
            self._minesMarked += 1
        
    def open(self,cell) :
        """ Abre una celda que está cerrada y sin marcar. Si la celda posee una mina la partida terminará. Si la celda
            ya esta abierta y su 'n' es <= 0 se abren de forma recursiva sus celdas vecinas cerradas y sin marcar """
        c = self.getCell(coordinates=cell)  

        if c.marked : 
            raise Exception("NO SE PUEDE ABRIR UNA CELDA MARCADA")       
        elif not c.opened : # Cerrada
            c.opened = True
            if c.mine : self._ended = True
        elif c.opened and c.n() > 0 :
            raise Exception("CELDA YA ABIERTA. NO SE PUEDEN ABRIR LAS CELDAS VECINAS POR NUMERO INSUFICIENTE DE MARCAS")       
        elif c.opened and c.n() <= 0 :
            for i in c.around :
                self.openRec(i)

    def openRec(self,cell) :
        """Abre de forma recursiva las celdas cerradas y sin marcar """
        if not cell.opened and not cell.marked :
            cell.opened = True
            if cell.mine :
                self._ended = True
            else :
                for i in cell.around :
                    self.openRec(i)

    def openAll(self) :
        """ Abre todas las celdas del tablero una vez la partida ha finalizado """
        for row in self._board :
            for cell in row :
                cell.opened = True

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
            
            if self.ended : self.openAll() #Abrir todas las celdas si la partida ha acabado
        except Exception :
            raise

    def boardHead(self) : 
        """ Obtiene la cabecera del tablero donde se indica las minas sin marcar, 
            las minas marcadas y el tiempo transcurrido  """       
        head = "MINAS RESTANTES: {} | MARCADAS: {} | TIEMPO: {:.4f} seg.\n\n" 

        return head.format(self.minesLeft,self.minesMarked,self.elapsedTime) 

    def __str__(self) :
        """ Obtiene una representación del tablero """
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
               rowStr.append(str(j))
               col += 1
            boardStr.append(' '.join(rowStr))
            rowStr = []
            row += 1
        
        return self.boardHead() + "\n\n".join(boardStr)
            

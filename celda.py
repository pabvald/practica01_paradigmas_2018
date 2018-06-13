class Celda:

    CSOM = u'\u2593' # ▒

    def __init__(self, c):
        """
           Constructor. Crea una Celda cerrada, sin marcar
           y conteniendo o no una mina según el parámetro
          c.
        """
        self.opened = False
        self.marked= False
        self.mine = True if c == '*' else False
        self.n = None
        
    def isMarked(self):
        return self.marked
  
    def isOpened(self):
        return self.opened
    
    def isClosed(self):
        return not self.opened
    
    def hasMine(self):
        return self.mine

    def setN(self,n):
        self.n = n
    
    def getChar(self):
        """
            Obtiene la representación de la Celda en 
            función de su estado.
        """
        if not self.opened and not self.marked :
            return self.CSOM 
        elif not self.opened and self.marked :
            return 'X'
        elif self.opened and self.n == 0 :
            return ' '
        elif self.opened and self.n < 0 :
            return '?'
        elif self.opened and self.n > 0:
            return chr(self.n)
        elif self.opened and self.marked and not self.mine :
            return '#'
        elif self.opened and not self.marked and self.mine :
            return '*'
        

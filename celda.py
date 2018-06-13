class Celda:

    CSOM = u'\u2593' # ▒

    def __init__(self, c):
        """
           Constructor. Crea una Celda cerrada, sin marcar
           y conteniendo o no una mina según el parámetro
          c.
        """
        self._opened = False
        self._marked= False
        self._mine = True if c == '*' else False
        self._n = None

    @property  
    def marked(self):
        return self._marked

    @marked.setter
    def marked(self,b) :
        self._marked = b

    @property
    def opened(self):
        return self._opened

    @opened.setter
    def opened(self, b):
        self._opened = b
    
    @property
    def mine(self):
        return self._mine

    @property
    def n(self):
        return self._n
    
    @n.setter
    def n(self,value):
        self._n = value
    
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
        

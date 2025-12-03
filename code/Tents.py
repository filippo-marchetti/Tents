from BoardGames import BoardGame

class Tents(BoardGame):
    def __init__(self):
        self._current_scheme = 0
        
        self._schemes = [
            "schemes/tents-2025-11-27-8x8-easy.txt",
            "schemes/tents-2025-11-27-8x8-medium.txt",
            "schemes/tents-2025-11-27-12x12-easy.txt",
            "schemes/tents-2025-11-27-12x12-medium.txt",
            "schemes/tents-2025-11-27-16x16-easy.txt",
            "schemes/tents-2025-11-27-16x16-medium.txt",
            "schemes/tents-2025-11-27-20x20-special.txt"
        ]
        
        self._grid = self.load_matrix(self._schemes[self._current_scheme])
        self._W = len(self._grid[0])
        self._H = len(self._grid)
        
        self._exceeded_row = []
        self._exceeded_col = []
        
        
    def play(self, x: int, y: int, action: str):
        match(action):
            case "toggle":
                if(self._grid[y][x] == "."): self._grid[y][x] = "A"
                elif(self._grid[y][x] == "A"): self._grid[y][x] = "G"
                elif(self._grid[y][x] == "G"): self._grid[y][x] = "."
            case "tent":
                self._grid[y][x] = "A"
            case "fill-grass":
                for i in range(1, self._H):
                    for j in range(1, self._W):
                        if(self._grid[i][j] == "."): self._grid[i][j] = "G"
            case "next_scheme":
                self._current_scheme = (self._current_scheme + 1) % len(self._schemes)
                self._grid = self.load_matrix(self._schemes[self._current_scheme])

                self._W = len(self._grid[0])
                self._H = len(self._grid)

                # RESET COMPLETO
                self._exceeded_row = []
                self._exceeded_col = []

                # Ricalcola subito le condizioni del nuovo schema
                self.getExceedRow()
                self.getExceedCol()
                                    
    def read(self, x: int, y: int) -> str: 
        return self._grid[y][x]
    
    def cols(self) -> int: 
        return self._W
    
    def rows(self) -> int:
        return self._H
    
    def getExceedRow(self) -> list:
        self._exceeded_row = []
        num_t = 0 # SERVE A CONTARE QUANTE TENDE CI SONO PER OGNI RIGA O COLONNA
        # RIGHE CON TENDE ECCEDENTI
        for y in range(1, self.rows()):
            num_t = 0
            for x in range(1, self.cols()):
                if self.read(x, y) == "A":
                    num_t += 1
            limit = int(self.read(0, y))
            if num_t > limit:
                self._exceeded_row.append(y)
        return self._exceeded_row
        
    def getExceedCol(self) -> list:   
        self._exceeded_col = []             
        num_t = 0 # SERVE A CONTARE QUANTE TENDE CI SONO PER OGNI RIGA O COLONNA
        
        # COLONNE CON TENDE ECCEDENTI
        for x in range(1, self.cols()):
            num_t = 0
            for y in range(1, self.rows()):
                if self.read(x, y) == "A":
                    num_t += 1
            limit = int(self.read(x, 0))
            if num_t > limit:
                self._exceeded_col.append(x)
        return self._exceeded_col
          
    def isNeighbor(self, x: int, y: int):
        check = [-1, 0, 1] # ARRAY CON LE VARIE DIREZIONI DA CONTROLLARE
        if(self.read(x, y) == "A"):
            for i in check:
                for j in check:
                    if(i == 0 and j == 0): continue
                    
                    if(0 <= x+i < self._W and 0 <= y+j < self._H):
                        if(self.read(x+i, y+j) == "A"):
                            return True
        return False
    
    def sigle_error(self, x: int, y: int) -> bool:
        if(self.isNeighbor(x, y) or y in self.getExceedRow() or x in self.getExceedCol()):
            return True
        else:
            return False
    
    def error(self) -> bool:
        n_check = False
        all_grass = True
        # CONTROLLO SE TUTTE LE TENDE HANNO UN VICINO E SE TUTTE LE CASELLE VUOTE SONO ERBA
        for x in range(1, self._W):
            for y in range(1, self._H):
                if(self.read(x, y) == "."): return True
                if(self.isNeighbor(x, y)): return True
        
        if(len(self.getExceedCol()) > 0 or len(self.getExceedRow())):
            return True
        
        return False
          
    def isWin(self) -> bool:
        check_grid = [row[:] for row in self._grid]
        dir = [(0, -1), (0, 1), (-1, 0), (1, 0)] # ARRAY CON LE 4 DIREZIONI DA CONTROLLARE
        
        # A OGNI ALBERO VIENE ASSOCIATA UNA SOLA TENDA, PER CONTROLLARLO CREO UNA NUOVA GRIGLIA
        # GLI ALBERI CHE RISPETTANO LE CONDIZIONI DI ASSOCIAZIONE CON LA TENDA DIVENTANO 'C'(CHECKED) 
        
        for x in range(0, self._W):
            for y in range(0, self._H):
                if(check_grid[y][x] == "T"):
                    found_tent = False
                    for k in dir:
                        i, j = k
                        
                        if(0 <= x+i < self._W and 0 <= y+j < self._H):
                            if(check_grid[y+j][x+i] == "A"):
                                found_tent = True
                                break
                                   
                    if(found_tent): check_grid[y][x] = "C"
                    else: return False
        
        num_tent = 0
        num_tree = 0
        
        for x in range(0, self._W):
            for y in range(0, self._H):
                if(check_grid[y][x] == "A"): num_tent += 1
                if(check_grid[y][x] == "C"): num_tree += 1
                if(check_grid[y][x] == "T"): return False
        
        if(num_tent != num_tree): return False
        
        return True
          
    def finished(self) -> bool:
        if(self.error()):
            return False
        elif(self.isWin()):
            return True
        else:
            return False
              
    def status(self) -> str:
        pass
    
    def load_matrix(self, scheme: str) -> list:
        mat = []
        try:
            # CARICAMENTO DELLO SCHEMA INIZIALE
            with open(scheme, "r") as file:
                for row in file:
                    mat.append(list(row.strip()))
        except:
            print("Attenzione: Errore nel caricamento dello schema")
            
        return mat
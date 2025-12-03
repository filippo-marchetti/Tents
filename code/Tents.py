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
                if(self._current_scheme + 1 < len(self._schemes)):self._current_scheme += 1
                else: self._current_scheme = 0
                
                self._grid = self.load_matrix(self._schemes[self._current_scheme])
                
                self._W = len(self._grid[0])
                self._H = len(self._grid)
                
            case "reset":
                self._grid = self.load_matrix(self._schemes[self._current_scheme])
                
                self._W = len(self._grid[0])
                self._H = len(self._grid)
            
            case "hint": # FA UNA SOLA AZIONE PER VOLTA
                solved_scheme = self.solve(self.check_moves(self.load_matrix(self._schemes[self._current_scheme])))
                
                for x in range(self.cols()):
                    for y in range(self.rows()):
                        if(solved_scheme[y][x] == "A" and self._grid[y][x] != "A"):
                            self._grid[y][x] = "A"
                            return
                        elif(solved_scheme[y][x] != "A" and self._grid[y][x] == "A"):
                            self._grid[y][x] = "."
                            return
            
                        
    def read(self, x: int, y: int) -> str: 
        return self._grid[y][x]
    
    def cols(self) -> int: 
        return self._W
    
    def rows(self) -> int:
        return self._H
    
    def getExceedRow(self, grid: list) -> list:
        exceeded_row = []
        num_t = 0 # SERVE A CONTARE QUANTE TENDE CI SONO PER OGNI RIGA O COLONNA
        # RIGHE CON TENDE ECCEDENTI
        for y in range(1, self.rows()):
            num_t = 0
            for x in range(1, self.cols()):
                if(grid[y][x] == "A"):
                    num_t += 1
            limit = int(grid[y][0])
            if(num_t > limit):
                exceeded_row.append(y)
        return exceeded_row
        
    def getExceedCol(self, grid: list) -> list:   
        exceeded_col = []             
        num_t = 0 # SERVE A CONTARE QUANTE TENDE CI SONO PER OGNI RIGA O COLONNA
        
        # COLONNE CON TENDE ECCEDENTI
        for x in range(1, self.cols()):
            num_t = 0
            for y in range(1, self.rows()):
                if(grid[y][x] == "A"):
                    num_t += 1
            limit = int(grid[0][x])
            if(num_t > limit):
                exceeded_col.append(x)
        return exceeded_col
          
    def isNeighbor(self, x: int, y: int, grid: list):
        check = [-1, 0, 1] # ARRAY CON LE VARIE DIREZIONI DA CONTROLLARE
        if(grid[y][x] == "A"):
            for i in check:
                for j in check:
                    if(i == 0 and j == 0): continue
                    
                    if(0 <= x+i < self._W and 0 <= y+j < self._H):
                        if(grid[y+j][x+i] == "A"):
                            return True
        return False
    
    def sigle_error(self, x: int, y: int) -> bool:
        if(self.isNeighbor(x, y, self._grid) or y in self.getExceedRow(self.getGrid()) or x in self.getExceedCol(self.getGrid())):
            return True
        else:
            return False
    
    def error(self) -> bool:
        # CONTROLLO SE TUTTE LE TENDE HANNO UN VICINO E SE TUTTE LE CASELLE VUOTE SONO ERBA
        for x in range(1, self._W):
            for y in range(1, self._H):
                if(self.read(x, y) == "."): return True
                if(self.isNeighbor(x, y, self._grid)): return True
        
        if(len(self.getExceedCol(self.getGrid())) > 0 or len(self.getExceedRow(self.getGrid()))):
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
    
    def is_valid(self,grid):
        tent = self.find_sol_tent(grid)
        
        for t in tent:
            x, y = t
            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    if(i == 0 and j == 0): continue
                    if(1 <= x+i < self._W and 1 <= y+j < self._H):
                        if(grid[y+j][x+i] == "A"):
                            return False
                        
        for x,y in tent:
            found = False
            for i,j in [(1,0),(-1,0),(0,1),(0,-1)]:
                c_x,c_y = x+i, y+j # CIRCONDARIO DELLA TENDA
                if(0 <= c_x < self._W and 0 <= c_y < self._H):
                    if(grid[c_y][c_x] == "T"):
                        found = True
                        break
            if(not found):
                return False
        
        if(len(self.getExceedCol(grid)) > 0 or len(self.getExceedRow(grid)) > 0):
            return False
        else:
            return True
        
    def solve(self, grid):
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if(grid[y][x] == "P"):
                    # PROVA A PIAZZARE LA TENDA
                    solver_grid = [row[:] for row in grid]
                    solver_grid[y][x] = "A"

                    # PROIBISCE IL PIAZZAMENTO DELLE TENDE INTORNO A QUELLA NUOVA
                    for i in [-1,0,1]:
                        for j in [-1,0,1]:
                            t_y, t_x = y+i, x+j
                            if(0 <= t_y < len(grid) and 0 <= t_x < len(grid[0])):
                                if(solver_grid[t_y][t_x] == "."):
                                    solver_grid[t_y][t_x] = "F"

                    # PIAZZAMENTO DI TENDE FINO A CHE NON CI SI IMBATTE IN UN ERRORE E SE CAPITA CAMBIA POSIZIONE PER LA TENDA
                    if(self.is_valid(solver_grid)):
                        result = self.solve(solver_grid)
                        if(result is not None):
                            return result

                    # SE LA TENDA E' STATA POSIZIONATO IN UNA POSIZIONE ERRATA VIENE CANCELLATA E LA SUA CASELLA PROIBITA IN UNA NUOVA GRIGLIA
                    updated_grid = [row[:] for row in grid] # NUOVA GRIGLIA COSTRUITA CON I PROCEDIMENTI DEL COMMENTO SOPRA
                    updated_grid[y][x] = "F"
                    if(self.is_valid(updated_grid)):
                        if len(self.find_sol_tent(grid)) > len(self.find_trees(grid)):
                            return None
                        result = self.solve(updated_grid)
                        if(result is not None):
                            return result

                    # TERMINA IL CICLO SE NON CI SONO SOLUZIONI CON LA P CORRENTE
                    return None

        # QUANDO NON RIMANGONO P VIENE ESEGUITO IL CONTROLLO FINALE
        if(self.is_valid(grid) and len(self.find_sol_tent(grid)) == len(self.find_trees(grid))):
            return grid  # SOLUZIONE FINALE
        
        return None
             
    def find_trees(self, grid) -> list:
        trees = []
        
        for x in range(self.cols()):
            for y in range(self.rows()):
                if(grid[y][x] == "T"): trees.append((x, y))

        return trees
    
    def find_sol_tent(self, grid) -> list:
        tent = []
        
        for x in range(self.cols()):
            for y in range(self.rows()):
                if(grid[y][x] == "A"): tent.append((x, y))

        return tent
    
    # CONTROLLA ED ELIMINA LE MOSSE A PRIORI SBAGLIATE
    def check_moves(self, grid: list):  
        dir = [(0, -1), (0, 1), (-1, 0), (1, 0)] # ARRAY CON LE 4 DIREZIONI DA CONTROLLARE
        trees = self.find_trees(grid)
        
        changed = True # SE AVVIENE UN CAMBIAMENTO IL CICLO SI RIPETE PER RIVEDERE LE MOSSE POSSIBILI
        
        while changed:
            changed = False 
            for t in trees:
                moves = []
                for d in dir:    
                    hint_tent_x = t[0] + d[0]
                    hint_tent_y = t[1] + d[1]
                    
                    if(1 <= hint_tent_x < len(grid[0]) and 1 <= hint_tent_y < len(grid)):
                        # CONTROLLO DELLE RIGHE E COLONNE IL CUI LIMITE E' ZERO
                        if(grid[0][hint_tent_x] == "0"): 
                            for i in range(1, len(grid)):
                                if(grid[i][hint_tent_x] == "." or grid[i][hint_tent_x] == "."): 
                                    grid[i][hint_tent_x] = "F" # CASELLE LA CUI POSIZIONE E' ESCLUSA
                                    changed = True 
                                
                                
                        elif(grid[hint_tent_y][0] == "0"): 
                            for j in range(1, len(grid[0])):
                                if(grid[hint_tent_y][j] == "." or grid[hint_tent_y][j] == "P"): 
                                    grid[hint_tent_y][j] = "F" # CASELLE LA CUI POSIZIONE E' ESCLUSA
                                    changed = True 

                        # CONTEGGIO DELLE MOSSE POSSIBILI PER ALBERO
                        if(grid[hint_tent_y][hint_tent_x] == "." or grid[hint_tent_y][hint_tent_x] == "P"): moves.append((hint_tent_y, hint_tent_x))
                
                # POSIZIONAMENTO DELLA TENDA NELL'UNICA POSIZIONE POSSIBILE PER QUELL'ALBERO        
                if(len(moves) == 1): 
                    s_y, s_x = moves[0]
                    grid[s_y][s_x] = "A" # A E' LA POSIZIONE DELLA TENDA SICURA
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            if(i == 0 and j == 0): continue
                            if(1 <= s_x+i < len(grid[0]) and 1 <= s_y+j < len(grid)):
                                if(grid[s_y+j][s_x+i] == "." or grid[s_y+j][s_x+i] == "P"):
                                    grid[s_y+j][s_x+i] = "F"
                                    changed = True
                # POSIZIONO P PER INDICARE POSIZIONI DELLE TENDE POSSIBILI
                for m in moves:
                    y, x = m
                    if(grid[y][x] == "."):
                        grid[y][x] = "P"
                        changed = True
                        
                        
        return grid
    
    def getGrid(self):
        return self._grid
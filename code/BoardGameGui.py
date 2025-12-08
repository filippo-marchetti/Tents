from Tents import Tents
import g2d

class BoardGameGui():
    def __init__(self, game: Tents, box_dim: int, text_dim: int, border_dim: int, canvas_dim: int, action: dict):
        self._game = game
        self._box_dim = box_dim
        self._text_dim = text_dim
        self._border_dim = border_dim
        self._canvas_dim = canvas_dim
        self._actions = action
    
    def gui(self):
        self.draw()
        
        if(self._game.finished()):
            victory_rect_dim =  self._canvas_dim / 4
            victory_rect_pos =  self._canvas_dim // 2 - (victory_rect_dim/2)
            
            g2d.set_color((255,255,255, 150))
            g2d.draw_rect((0 , victory_rect_pos), (self._canvas_dim, victory_rect_dim))
            
            g2d.set_color((0,0,0))
            g2d.draw_text("Congratulazioni! Hai risolto lo schema", (self._canvas_dim //2, self._canvas_dim //2), 50)
        
        # X E Y DEL CURSORE
        mouse_x, mouse_y = g2d.mouse_pos()
        clicked_x = int((mouse_x) // self._box_dim)
        clicked_y = int((mouse_y) // self._box_dim)
        
        # CICLO TENDA/ERBA/NIENTE AL CLICK
        if(g2d.mouse_clicked()):
            if(clicked_x < self._game.cols() and clicked_y < self._game.rows()):
                self._game.play(clicked_x, clicked_y, "toggle")

        # CONTROLLO SE VENGONO PREMUTI TASTI E ESEGUO LA RELATIVA FUNZIONE
        for key, action in self._actions.items():
            if(g2d.key_pressed(key) and clicked_x < self._game.cols() and clicked_y < self._game.rows()):
                self._game.play(clicked_x, clicked_y, action)
            if(key == "n"): 
                self.recalc_layout()
        
    def draw(self):
        for x in range(0, self._game.cols(), 1):
            for y in range(0, self._game.rows(), 1):
                #CALCOLO DELLA POSIZIONE DEL QUADRATO
                pos_x = self._box_dim*x
                pos_y = self._box_dim*y
                
                #POSIZIONE DEL TESTO
                text_pos_x = pos_x + (self._box_dim // 2)
                text_pos_y = pos_y + (self._box_dim // 2)
                
                # I NUMERI VENGONO COLORATI DI ROSSO SE VI SONO TROPPE TENDE IN QUELLA COLONNA O RIGA
                if((x == 0 or y == 0) and x != y): # STAMPA DEI NUMERI 
                    if(x == 0):
                        if(y in self._game.getExceedRow(self._game.getGrid())):
                            g2d.set_color((255,0,0))
                        else: g2d.set_color((0,0,0))
                        
                    else:  
                        if(x in self._game.getExceedCol(self._game.getGrid())):
                            g2d.set_color((255,0,0))
                        else: g2d.set_color((0,0,0))
                    
                    g2d.draw_text(self._game.read(x, y), (text_pos_x, text_pos_y), self._text_dim)
                        
                elif(x > 0 and y > 0): # STAMPA DELLA GRIGLIA
                    g2d.set_color((0,0,0), self._border_dim)
                    g2d.draw_rect((pos_x, pos_y), (self._box_dim, self._box_dim))
                
                content = self._game.read(x, y)
                
                rect_dim = self._box_dim - self._border_dim*2
                
                # IL COLORE DELLE CASELLE VIENE DALLO SFONDO IL MAIN.PY
                match(content):
                    case ".": 
                        if(x != 0 and y != 0):
                            g2d.set_color((255,255,255))
                            g2d.draw_rect((pos_x+self._border_dim, pos_y+self._border_dim), (rect_dim,rect_dim))
                    case "T": # ALBERO
                        g2d.set_color((20,170,80)) 
                        g2d.draw_rect((pos_x+self._border_dim, pos_y+self._border_dim),(rect_dim, rect_dim))
                        g2d.set_color((0,0,0))
                        g2d.draw_text("🌲", (text_pos_x, text_pos_y), self._box_dim)
                    case "A": # TENDA     
                        g2d.set_color((20,170,80)) 
                        g2d.draw_rect((pos_x+self._border_dim, pos_y+self._border_dim),(rect_dim, rect_dim))                   
                        if(self._game.sigle_error(x, y)):
                            g2d.set_color((255,0,0))
                            g2d.draw_text("⛺", (text_pos_x, text_pos_y), self._box_dim)
                        else:
                            g2d.set_color((0,0,0))
                            g2d.draw_text("⛺", (text_pos_x, text_pos_y), self._box_dim)
                    case "G": # ERBA
                        g2d.set_color((20,170,80)) 
                        g2d.draw_rect((pos_x+self._border_dim, pos_y+self._border_dim),(rect_dim, rect_dim))
                                                
        # STAMPA DEL BORDO ESTERNO PER FARE IN MODO CHE TUTTE LE LINEE SIANO SPESSE UGUALE
        g2d.set_color((0,0,0), self._border_dim*2)
        g2d.draw_rect((self._box_dim, self._box_dim), (self._box_dim*(self._game.cols()-1), self._box_dim*(self._game.rows()-1)))
        
    def recalc_layout(self):
        # RICALCOLO LA DIMENSIONE DEL BOX OGNI VOLTA CHE CAMBIA LO SCHEMA
        self._box_dim = (self._canvas_dim)/max(self._game.rows(), self._game.cols())
        self._text_dim = int(self._box_dim * 0.6)
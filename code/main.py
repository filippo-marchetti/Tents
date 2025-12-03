from Tents import Tents
import g2d
from BoardGameGui import BoardGameGui

def tick():
    g2d.clear_canvas((20,170,80))

    gui.gui()
    
def main():
    global gui

    game = Tents()
    
    box_dim = 40 # DIMESIONE DI UNA SINGOLA CASELLA NELLA GRIGLIA
    CANVAS_DIM = max(1000,box_dim*max(game.cols(), game.rows()))
    shift_x = (CANVAS_DIM - box_dim*game.cols()) // 2  # GRIGLIA MESSA AL CENTRO ORIZZONTALMENTE
    text_dim = int(box_dim*0.6) # DIMENSIONE TESTO
    border_dim = 1 # DIMENSIONE TESTO
    
    g2d.init_canvas((CANVAS_DIM, CANVAS_DIM))
    
    actions = {
        "t": "tent",
        "g": "fill-grass",
        "a": "hint",
        "n": "next_scheme",
        "r": "reset"
    }
    
    gui = BoardGameGui(game, box_dim, shift_x, text_dim, border_dim, CANVAS_DIM, actions)
    
    g2d.main_loop(tick, 30)
    
main()
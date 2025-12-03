from Tents import Tents
import g2d
from BoardGameGui import BoardGameGui

CANVAS_DIM = 1300

def tick():
    g2d.clear_canvas((20,170,80))

    gui.gui()
    
def main():
    global gui
    
    g2d.init_canvas((CANVAS_DIM, CANVAS_DIM))
    
    game = Tents()
    
    box_dim = min((CANVAS_DIM // 1.5)//(game.cols()), 50) # DIMESIONE DI UNA SINGOLA CASELLA NELLA GRIGLIA
    shift_x = (CANVAS_DIM - box_dim*game.cols()) // 2  # GRIGLIA MESSA AL CENTRO ORIZZONTALMENTE
    text_dim = int(box_dim*0.6) # DIMENSIONE TESTO
    border_dim = 1 # DIMENSIONE TESTO
    
    actions = {
        "t": "tent",
        "g": "fill-grass",
        "a": "hint",
        "n": "next_scheme"
    }
    
    gui = BoardGameGui(game, box_dim, shift_x, text_dim, border_dim, CANVAS_DIM, actions)
    
    g2d.main_loop(tick, 30)
    
main()
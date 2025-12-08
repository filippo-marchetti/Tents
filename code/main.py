from Tents import Tents
import g2d
from BoardGameGui import BoardGameGui

def tick():
    g2d.clear_canvas((20,60,110))

    gui.gui()
    
def main():
    global gui

    game = Tents()
    
    CANVAS_DIM = 899
    box_dim = (CANVAS_DIM)/max(game.rows(), game.cols()) # DIMESIONE DI UNA SINGOLA CASELLA NELLA GRIGLIA
    text_dim = int(box_dim*0.6) # DIMENSIONE TESTO
    border_dim = 1 # DIMENSIONE TESTO
    
    g2d.init_canvas((CANVAS_DIM, CANVAS_DIM))
    
    actions = {
        "t": "tent",
        "g": "fill-grass",
        "a": "hint",
        "n": "next_scheme",
        "b": "previous_scheme",
        "r": "reset"
    }
    
    gui = BoardGameGui(game, box_dim, text_dim, border_dim, CANVAS_DIM, actions)
    
    g2d.main_loop(tick, 30)
    
main()
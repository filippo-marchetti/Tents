from Tents import Tents

def test_toggle():
    game = Tents()
    x, y = 1, 1
    game._grid[y][x] = "."

    game.play(x, y, "toggle")
    if(game.read(x, y) != "A"):
        print("ERRORE test_toggle fallito: cambio a A non eseguito")
        return
    game.play(x, y, "toggle")
    if(game.read(x, y) != "G"):
        print("ERRORE test_toggle fallito: cambio a G non eseguito")
        return
    game.play(x, y, "toggle")
    if(game.read(x, y) != "."):
        print("ERRORE test_toggle fallito: cambio a . non eseguito")
        return
    print("SUCCESSO test_toggle corretto")

def test_fill_grass():
    game = Tents()
    for i in range(1, game.rows()):
        for j in range(1, game.cols()):
            game._grid[i][j] = "."
    game.play(0, 0, "fill-grass")

    success = True
    for i in range(1, game.rows()):
        for j in range(1, game.cols()):
            if(game.read(j, i) != "G"):
                success = False
                break
    if(success):
        print("SUCCESSO test_fill_grass corretto")
    else:
        print("ERRORE test_fill_grass fallito")

def test_next_scheme():
    game = Tents()
    initial_grid = [row[:] for row in game.getGrid()]
    game.play(0, 0, "next_scheme")
    if(game.getGrid() == initial_grid):
        print("ERRORE test_next_scheme fallito")
        return
    else:
        print("SUCCESSO test_next_scheme corretto")
        
def test_solve():
    game = Tents()
    game._grid = [
        ["0", "1", "1"],
        ["1", ".", "T"],
        ["1", ".", "."]
    ]
    game._W = len(game._grid[0])
    game._H = len(game._grid)
    tree_x, tree_y = 2, 1

    solved_grid = game.solve(game.check_moves([row[:] for row in game._grid]))
    if solved_grid is None:
        print("ERRORE test_solve fallito: nessuna soluzione")
        return

    # Controlliamo che ci sia una tenda accanto all'albero
    tent_pos = game.find_sol_tent(solved_grid)
    if len(tent_pos) != 1:
        print("ERRORE test_solve fallito: numero sbagliato di tende")
        return

    t_x, t_y = tent_pos[0]
    
    if abs(t_x - tree_x) + abs(t_y - tree_y) != 1:
        print("ERRORE test_solve fallito: tenda non adiacente all'albero")
        return
    
    print("SUCCESSO test_solve corretto")


test_toggle()
test_fill_grass()
test_next_scheme()
test_solve()


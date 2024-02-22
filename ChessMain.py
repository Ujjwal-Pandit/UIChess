"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState object.
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512 #400 is another good option
DIMENSION = 8 #dimensions are 8x8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15 #for animation later on
IMAGES = {}

"""
Initialize a global dictionary of images. This will be called exactly once in the main
"""

def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".svg"), (SQ_SIZE*3.4, SQ_SIZE*3.4))
    #NOTE: we can access an image by saying 'IMAGES['wp']'


"""
The main driver for our code. This will handle user input and updating the graphics.
"""

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable when a move is made
    loadImages() # only do this once, before the while loop
    running = True
    sqSelected = () # no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerClicks = [] # keep track of payer clicks (two tuples: [(6,4), (4,4)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x,y) location of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): # user clicked the same square twice
                    sqSelected = () # deselect
                    playerClicks = [] # clears the player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) # we append for both 1st and 2nd clicks
                # was that the user's second click
                if len(playerClicks) == 2: # after the 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqSelected = () #reset user clicks
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

"""
It is responsible for all the graphics within the current game state"""
def drawGameState(screen, gs):
    drawBoard(screen) # draw squares on the board
    # add in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board) # draw pieces on top of those squares

"""
Draw the squares on the board. The top left square is always light
"""
def drawBoard(screen):
    colors = [p.Color(217,229,249), p.Color(102,129,178)] # Icy Sea: https://www.color-hex.com/color-palette/94676
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
"""
Draw the pieces on the board using the current GameState.board
"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": # not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()


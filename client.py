from network import Network
import pygame

WIDTH, HEIGHT, GRID_WIDTH, GRID_HEIGHT = 768, 432, 390, 390
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
GRID_SURFACE = pygame.Surface((GRID_HEIGHT, GRID_WIDTH))
pygame.display.set_caption("Thicc Thacc Toes Online")
pygame.font.init()

# Colors
class Palette:
    def __init__(self) -> None:
        self.grid_line = (255, 255, 255)
        self.bg = (194, 194, 194)
        self.gridBg = (44, 44, 44)
        self.gridHover = (55, 55, 55)
        self.blue = (28, 164, 252)
        self.orange =(90, 62, 40)

class Button:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def is_Hovering(self, pos):
        if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(pos):
            return True
        else:
            return False

    def get_Rect(self):
        return (self.x, self.y, self.width, self.height)

def draw_window(btns_to_draw, game, grid_btns, myTurn, last_winner=None):
    WIN.fill(Palette().bg)

    GRID_SURFACE.fill(Palette().gridBg)
    # Draw grid lines
    pygame.draw.line(GRID_SURFACE, Palette().grid_line, (0, GRID_HEIGHT / 3), (WIDTH, GRID_HEIGHT / 3), 10)
    pygame.draw.line(GRID_SURFACE, Palette().grid_line, (0, GRID_HEIGHT / 3 * 2), (WIDTH, GRID_HEIGHT / 3 * 2), 10)
    pygame.draw.line(GRID_SURFACE, Palette().grid_line, (GRID_WIDTH / 3, 0), (GRID_WIDTH / 3, GRID_HEIGHT), 10)
    pygame.draw.line(GRID_SURFACE, Palette().grid_line, (GRID_WIDTH / 3 * 2, 0), (GRID_WIDTH / 3 * 2, GRID_HEIGHT), 10)

    # Add the whole grid to the main Surface
    WIN.blit(GRID_SURFACE, (WIDTH / 2 - GRID_WIDTH / 2, HEIGHT / 2 - GRID_HEIGHT / 2))

    # Draw the "preview" of the hovering button
    for btn in btns_to_draw:
        pygame.draw.rect(WIN, btn.color, btn.get_Rect(), border_radius=10)

    # Draw the "x"s and "o"s
    if game != None:
        count = 0
        thickness = 4
        grid = game.grid
        for i in range(len(grid)):
            for j in range(len(grid)):
                symbol = grid[i][j]
                btn = grid_btns[count]
                if symbol == "o": 
                    pygame.draw.circle(WIN, Palette().blue, (btn.x + btn.width / 2, btn.y + btn.height / 2), btn.width / 2, thickness)
                elif symbol == "x":
                    pygame.draw.line(WIN, Palette().blue, (btn.x, btn.y), (btn.x + btn.width, btn.y + btn.height), thickness * 2)
                    pygame.draw.line(WIN, Palette().blue, (btn.x, btn.y + btn.height), (btn.x + btn.width, btn.y), thickness * 2)
                count += 1

    draw_turn(myTurn)
    draw_status(last_winner)

    pygame.display.flip()

def draw_turn(myTurn:bool):
    """Show on the side whether it's your turn or your opponent's"""
    font = pygame.font.SysFont("comicsans", 32)
    if myTurn:
        text = font.render("Your turn! :)", 1, Palette().gridBg)
        WIN.blit(text, (189 - text.get_width() - (text.get_width() / 2 / 2), GRID_HEIGHT / 2))
    else:
        text = font.render("Opponent's Turn", 1, Palette().gridBg)
        WIN.blit(text, (189 - text.get_width() - ((189 - text.get_width()) / 2), GRID_HEIGHT / 2))

def draw_status(last_winner=None):
    """Draw who won the last game"""
    font = pygame.font.SysFont("comicsans", 32)
    if last_winner:
        text = font.render(f"Last Winner: {last_winner.upper()}", 1, Palette().gridBg)
        WIN.blit(text, (WIDTH - text.get_width() - (189 - text.get_width()) / 2, GRID_HEIGHT / 2))


def draw_winner(msg:str):
    font = pygame.font.SysFont("comicsans", 72)
    text = font.render(msg, 1, Palette().orange)
    WIN.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

    pygame.display.flip()
    pygame.time.delay(1000)

def grid_is_full(grid):
    count = 0
    for line in grid:
        if -1 not in line:
            count += 1
    
    if count == 3: 
        return True
    return False

grid_btns = []

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    game = None
    myTurn = False

    # Create the grid's buttons
    padding = 10
    offset_x = 189 + padding
    offset_y = 21 + padding
    btn_color = Palette().gridHover
    for x in range(3):
        for y in range(3):
            if x == 0 and y == 0:
                grid_btns.append(Button(offset_x, offset_y, 105, 105, btn_color))

            elif y == 0:
                grid_btns.append(Button(offset_x + GRID_WIDTH / 3 * y, offset_y + (padding / 2) + GRID_WIDTH / 3 * x, 105, 105, btn_color))

            elif x == 0:
                grid_btns.append(Button(offset_x + + (padding / 2) + GRID_WIDTH / 3 * y, offset_y  + GRID_WIDTH / 3 * x, 105, 105, btn_color))

            else:
                grid_btns.append(Button(offset_x + padding / 2 + GRID_WIDTH / 3 * y, offset_y + padding / 2 + GRID_WIDTH / 3 * x, 105, 105, btn_color))

    while run:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        data = n.recvGame() # Attempt to get the grid

        if data != None:
            game = data

            p1_won = game.checkWin("x")
            p2_won = game.checkWin("o")

        if p1_won: # Someone won
            winner_txt = "Player X Won!"
            game.last_winner = "X"
            draw_winner(winner_txt)
            n.send("WINNER_X")
            continue
        elif p2_won:
            winner_txt = "Player O Won!"
            game.last_winner = "O"
            draw_winner(winner_txt)
            n.send("WINNER_O")
            continue
        elif game != None and grid_is_full(game.grid): # Grid is full, no one won.
            game.last_winner = "DRAW"
            n.send("WINNER_DRAW")
            continue
        else:
            # Check if its my turn
            if game != None and game.turnP1 == True and n.getSymbol() == 0:
                myTurn = True
            elif game != None and game.turnP1 == False and n.getSymbol() == 1:
                myTurn = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        
                        if myTurn:
                            # Get the "status" of the tiles
                            empty_tiles = [False] * len(grid_btns)
                            counter = 0
                            for i in range(game.rows):
                                for j in range(game.cols):
                                    if game.grid[i][j] == -1:
                                        empty_tiles[counter] = True  
                                    counter += 1
                            
                            # Check if we are clicking a tile in the grid
                            for btn in range(len(grid_btns)):
                                if grid_btns[btn].is_Hovering(mouse_pos) and empty_tiles[btn]:
                                    data = n.send(str(btn))
                                    if data != None:
                                        game = data
                                    print(game.grid) # TODO : Remove that bad boi
                                    break
                            myTurn = False

            btns_to_draw = []

            # Check for the buttons we are hovering
            for btn in grid_btns:
                if btn.is_Hovering(mouse_pos):
                    btns_to_draw.append(btn)

            draw_window(btns_to_draw, game, grid_btns, myTurn, game.last_winner)
        

main()


import threading
import socket
import pickle
from game import Game

HOST = socket.gethostbyname(socket.gethostname())
PORT = 3000
ADDR = (HOST, PORT)

games = {}
idCount = 0

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(ADDR)
except socket.error as e:
    print(e)

server.listen()
print(f"Server started on port {PORT}")

def reset_game(game, winner):
    game.resetGame()
    game.last_winner = winner

    return game

def handle_client(conn:socket.socket, player, gameId):
    global idCount

    # Send to the player what symbol he is
    print(player)
    conn.send(str.encode(str(player)))

    reply = ""
    while True:
        try:
            data = conn.recv(1024).decode()
        except:
            break

        if gameId in games:
            game = games[gameId]

            if not data:
                break

            try: # The client sent a position in the grid
                number = int(data)
                if player == 0 and game.turnP1 == False or player == 1 and game.turnP1 == True: # Not your turn baka
                    conn.sendall(pickle.dumps(None))

                symbol = "x"
                if player != 0:
                    symbol = "o"

                game.placeSymbol(number, symbol)
                game.turnP1 = not game.turnP1 # Switch to the other player's turn

                conn.sendall(pickle.dumps(game))
                
            except ValueError: # The client sent something else
                if data == "GET_GAME":
                    conn.sendall(pickle.dumps(game))
                elif data == "RESET_GAME": # TODO: Enlever ce bad boi
                    game.resetGame() 
                    conn.sendall(pickle.dumps(game))
                elif data == "WINNER_X":
                    game = reset_game(game, "X")
                    conn.sendall(pickle.dumps(game))
                elif data == "WINNER_O":
                    game = reset_game(game, "O")
                    conn.sendall(pickle.dumps(game))
                elif data == "WINNER_DRAW":
                    game = reset_game(game, "-")
                    conn.sendall(pickle.dumps(game))

        else:
            break
    
    # A player disconnected or lost connection
    print("Lost connection.")
    try:
        del games[gameId]
        print(f"Closing game {gameId}")
    except:
        pass
    idCount -= 1
    conn.close()

while True:
    conn, addr = server.accept()

    idCount += 1
    player = 0
    gameId = (idCount - 1) // 2 
    if idCount % 2 == 1: # Basically creates a game if a odd number of people are connected to server
        games[gameId] = Game(gameId)
        print("Creating a game...")
    else:
        games[gameId].ready = True
        player = 1

    thread = threading.Thread(target=handle_client, args=(conn, player, gameId))
    thread.start()

    
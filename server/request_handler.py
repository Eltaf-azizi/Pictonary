import socket
import threading
import json


class Server:
    PLAYERS = 4  # Number of players needed to start a game

    def __init__(self):
        self.connection_queue = []  # Queue to manage waiting players
        self.gameId = 0  # Unique game ID counter

    def player_thread(self, conn, player):
        """
        Handles communication with an individual player.
        """
        while True:
            try:
                # Receive data from client
                data = conn.recv(1024)
                if not data:
                    break  # Exit loop if no data is received

                # Process client request
                data = json.loads(data.decode())
                send_msg = {key: [] for key in data.keys()}  # Example processing logic

                # Send response back to the client
                send_msg = json.dumps(send_msg)
                conn.sendall((send_msg + ".").encode())

            except json.JSONDecodeError as e:
                print(f"[ERROR] Failed to decode JSON from {player.get_name()}: {e}")
                break
            except Exception as e:
                print(f"[EXCEPTION] {player.get_name()} disconnected: {e}")
                break

        # Handle disconnection
        if player.game:
            player.game.player_disconnected(player)

        if player in self.connection_queue:
            self.connection_queue.remove(player)

        print(f"[DISCONNECT] {player.name} disconnected.")
        conn.close()

    def handle_queue(self, player):
        """
        Adds players to the queue and starts a game when enough players are available.
        """
        from game import Game  # Lazy import to avoid circular dependency

        self.connection_queue.append(player)
        print(f"[QUEUE] Player {player.get_name()} added to queue.")
        if len(self.connection_queue) >= self.PLAYERS:
            game = Game(self.gameId, self.connection_queue[:])  # Create a new game
            for p in game.players:
                p.set_game(game)  # Assign game to players

            self.gameId += 1
            self.connection_queue = []
            print(f"[GAME] Game {self.gameId - 1} started...")

    def authentication(self, conn, addr):
        """
        Handles player authentication and starts the player thread.
        """
        from player import Player  # Lazy import to avoid circular dependency

        try:
            # Receive player name
            data = conn.recv(1024)
            name = data.decode().strip()  # Strip any whitespace
            if not name:
                raise ValueError("No name received")

            conn.sendall("1".encode())  # Acknowledge connection
            player = Player(addr, name)  # Create a player instance
            print(f"[AUTH] Player {name} authenticated.")
            self.handle_queue(player)

            # Start a thread for the player
            thread = threading.Thread(target=self.player_thread, args=(conn, player))
            thread.start()

        except ValueError as e:
            print(f"[ERROR] Authentication failed: {e}")
            conn.close()
        except Exception as e:
            print(f"[EXCEPTION] Unexpected error during authentication: {e}")
            conn.close()

    def connection_thread(self):
        """
        Starts the server and listens for incoming connections.
        """
        server = "127.0.0.1"  # Use localhost for the server
        port = 5556

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((server, port))
            s.listen()
            print(f"Server started on {server}:{port}, waiting for connections...")
        except socket.error as e:
            print(f"[ERROR] Failed to bind to {server}:{port}: {e}")
            return

        while True:
            try:
                conn, addr = s.accept()
                print(f"[CONNECT] New connection from {addr}")
                self.authentication(conn, addr)
            except Exception as e:
                print(f"[ERROR] Connection error: {e}")


if __name__ == "__main__":
    try:
        s = Server()
        thread = threading.Thread(target=s.connection_thread, daemon=True)  # Daemon thread to allow graceful exit
        thread.start()
        print("Server is running. Press Ctrl+C to stop.")
        thread.join()  # Keep the main thread alive
    except KeyboardInterrupt:
        print("\nServer shutting down.")

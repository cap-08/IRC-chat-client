import socket
import threading
import argparse
from datetime import datetime

# ANSI colors
GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"

class IRCClient:
    def __init__(self, server, port, nick, channel):
        self.server = server
        self.port = port
        self.nick = nick
        self.channel = channel
        self.connected = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        print(f"{BLUE}Connecting to {self.server}:{self.port}...{RESET}")
        self.sock.connect((self.server, self.port))
        self.connected = True

        self.send_cmd(f"NICK {self.nick}")
        self.send_cmd(f"USER {self.nick} 0 * :{self.nick}")

        self.join_channel(self.channel)

        threading.Thread(target=self.listen, daemon=True).start()

    def send_cmd(self, cmd):
        self.sock.send((cmd + "\r\n").encode())

    def join_channel(self, channel):
        self.channel = channel
        self.send_cmd(f"JOIN {channel}")
        print(f"{GREEN}Joined {channel}{RESET}")

    def listen(self):
        buffer = ""
        while self.connected:
            data = self.sock.recv(2048).decode(errors="ignore")
            buffer += data

            while "\r\n" in buffer:
                line, buffer = buffer.split("\r\n", 1)
                self.handle_server_msg(line.strip())

    def handle_server_msg(self, msg):
        if msg.startswith("PING"):
            token = msg.split(" ", 1)[1]
            self.send_cmd(f"PONG {token}")
            print(f"{BLUE}[Server] PING → PONG {token}{RESET}")
            return

        parts = msg.split(" ")
        if len(parts) < 2:
            return

        command = parts[1]

        if command == "PRIVMSG":
            prefix = parts[0]
            sender = prefix.split("!")[0][1:]
            channel = parts[2]
            text = " ".join(parts[3:])[1:]
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"{GREEN}[{timestamp}] <{sender}> {text}{RESET}")

        elif command == "JOIN":
            user = parts[0][1:].split("!")[0]
            channel = parts[2][1:] if len(parts) > 2 else self.channel
            print(f"{BLUE}{user} joined {channel}{RESET}")

        elif command == "QUIT":
            user = parts[0][1:].split("!")[0]
            print(f"{RED}{user} quit{RESET}")

    def send_message(self, text):
        if self.channel:
            self.send_cmd(f"PRIVMSG {self.channel} :{text}")

    def quit(self):
        self.send_cmd("QUIT :Bye")
        self.connected = False
        self.sock.close()
        print(f"{RED}Disconnected{RESET}")

def user_input_loop(client):
    while client.connected:
        try:
            text = input()
            if text.startswith("/join"):
                _, ch = text.split(" ", 1)
                client.join_channel(ch.strip())
            elif text.startswith("/quit"):
                client.quit()
                break
            else:
                client.send_message(text)
        except KeyboardInterrupt:
            client.quit()
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Minimal IRC Client")
    parser.add_argument("--server", default="irc.libera.chat")
    parser.add_argument("--port", type=int, default=6667)
    parser.add_argument("--nick", default="JacobBot")
    parser.add_argument("--channel", default="#test")

    args = parser.parse_args()

    client = IRCClient(args.server, args.port, args.nick, args.channel)
    client.connect()

    print(f"{BLUE}Type messages or commands: /join #channel, /quit{RESET}")
    user_input_loop(client)

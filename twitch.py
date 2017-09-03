import socket
import pyautogui
import json

with open('token.json') as f:
    data = json.load(f)

SERVER = "irc.twitch.tv"
PORT = 6667
PASS = data["key"]
BOT = "TWITCHBOT"
CHANNEL = "second_eye_blind"
OWNER = "second_eye_blind"

class TwitchBot:
    def __init__(self, game, approved_commands):
        self.game = game
        self.approved_commands = approved_commands
        self.message = ""


    def game_control(self):
        message = self.message
        if message in self.approved_commands:
            pyautogui.press(message)
        elif "+" in message:
            try:
                commands = message.split("+")
                if set(commands).issubset(set(self.approved_commands)):
                    pyautogui.hotkey(commands[0], commands[1])
            except:
                self.message = ""
        else:
            try:
                commands = message.split(" ")
                num = int(commands[0])
                direction = commands[1] if commands[1] in self.approved_commands else None
                num = num if num <= 20 else 20
                for i in range(num):
                    pyautogui.press(commands[1])
            except:
                    self.message = ""
        self.message = ""

    def join_chat(self):
        loading = True
        while loading:
            readbuffer_join = irc.recv(1024)
            readbuffer_join = readbuffer_join.decode()
            for line in readbuffer_join.split("\n")[0:-1]:
                print(line)
                loading = loadingComplete(line)

    def loadingComplete(self, line):
        if ("End of /NAMES list" in line):
            print("Bot has joined " + CHANNEL + "'s Channel'")
            return False
        else:
            return True

    def sendMessage(self, irc, message):
        messageTemp =  "PRIVMSG #" + CHANNEL + " :" + message
        irc.send((messageTemp + "\n").encode())

    def getUser(self, line):
        separate = line.split(":", 2)
        user = separate[1].split("!", 1)[0]
        return user

    def getMessage(self, line):
        try:
            self.message = (line.split(":",2))[2].lower()
        except:
            self.message = ""


    def console(self, line):
        if "PRIVMSG" in line:
            return False
        return True

    def startSession(self):
        irc = socket.socket()
        irc.connect((SERVER, PORT))
        irc.send(("PASS " + PASS + "\n" + "NICK " + BOT + "\n" + "JOIN #" + CHANNEL + "\n").encode())
        while True:
            try:
                readbuffer = irc.recv(1024).decode()
            except:
                readbuffer = ""

            for line in readbuffer.split("\r\n"):
                if line == "":
                    continue
                elif "PING" in line and self.console(line):
                    msg = "PONG tmi.twitch.tv\r\n".encode()
                    irc.send(msg)
                    print(msg)
                    continue
                else:
                    # user = twitch.getUser(line)
                    print(line)
                    self.getMessage(line)
                    self.game_control()

if __name__ == '__main__':

    twitch = TwitchBot("Crypt of the Necrodancer", ["left", "right", "up", "down", "enter"])
    twitch.startSession()

import time
from mcstatus import JavaServer
from dotenv import load_dotenv
import os

from joinNotif import newPlayersCheck
# from databaseRequests import readData, writeRecord

def log(msg):
    print(msg)
    with open("log.txt", "a") as f:
        f.write(msg + "\n")

def checkingLoop(serverIP):
    TOTAL_ATTEMPTS = 5
    server = JavaServer.lookup(serverIP)
    prevPlayers = []

    while True:
        for attempt in range(TOTAL_ATTEMPTS):
            currentTime = time.strftime('%I:%M:%S %p')
            try:
                status = server.status()
                latency = status.latency
                motdPlain = status.motd.to_plain().lower()

                if "server not found" in motdPlain:
                    log(f"[{currentTime}] Server not Found! Aborting completely. | Ping: {latency:.2f}ms")
                    exit()
                elif "offline" in motdPlain:
                    log(f"({attempt + 1}) [{currentTime}] Server is Offline | Ping: {latency:.2f}ms")
                else:
                    playersSample = status.players.sample
                    players = [player.name for player in playersSample] if playersSample else []
                    newPlayersOnline: bool = newPlayersCheck(prevPlayers, players)

                    log(f"({attempt+1}) [{currentTime}] Online: {players} {'(New Players!!)' if newPlayersOnline else ''} | Ping: {latency:.2f}ms")

                    prevPlayers = players

                break

            except ConnectionResetError:
                if attempt < 4:
                    time.sleep(2)
                else:
                    log(f"({attempt+1}) [{currentTime}] Aborting status check for this minute because server is unreachable.")

            except Exception as e:
                if attempt < 4:
                    log(f"[{currentTime}] Attempt {attempt+1} failed: {type(e).__name__} {e}. Retrying in 2s...")
                    time.sleep(2)
                else:
                    log(f"({attempt+1}) Aborting status check for this minute because ran out of attempts. Error: {e}.")

        time.sleep(60)

if __name__ == '__main__':
    load_dotenv()
    SERVER_IP = os.getenv("SERVER_IP")
    if SERVER_IP:
        print(f"Server IP Loaded: {SERVER_IP}")
    else:
        raise Exception("Server IP not found in ENV!")

    log("\nMonitoring started... (Ctrl+C to stop)")
    checkingLoop(SERVER_IP)
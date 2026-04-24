import time
from mcstatus import JavaServer
from dotenv import load_dotenv
import os

from joinNotif import newPlayersCheck
from databaseRequests import readData, writeRecord
from record import Record

def log(msg):
    print(msg)
    with open("log.txt", "a") as f:
        f.write(msg + "\n")

def serverStatus(server: JavaServer, currentRecord: Record):
    TOTAL_ATTEMPTS = 5
    for attempt in range(TOTAL_ATTEMPTS):
        currentRecord.attempts = attempt + 1

        try:
            return server.status()

        except Exception as e:
            if attempt < 4:
                time.sleep(2)
            else:
                log(f"({attempt + 1}) [{currentRecord.attempts}] Aborting status check for this minute because ran out of attempts. {type(e).__name__}: {e}.")
                currentRecord.error = f"{type(e).__name__}: {e}"
                return None

def processStatusData(status, currentRecord: Record, prevPlayers: list) -> list: # (Returns player list)
    currentRecord.ping = round(status.latency, 2)
    currentRecord.amountOnline = status.players.online
    motdPlain = status.motd.to_plain().lower()

    if "server not found" in motdPlain:
        log(f"[{currentRecord.time}] Server not Found! Aborting completely. | Ping: {currentRecord.ping}ms")
        exit()

    elif "offline" in motdPlain:
        log(f"({currentRecord.attempts}) [{currentRecord.time}] Server is Offline | Ping: {currentRecord.ping}ms")
        currentRecord.onlineStatus = "Offline"
        return prevPlayers

    else:
        currentRecord.onlineStatus = "Online"

        playersSample = status.players.sample
        players = [player.name for player in playersSample] if playersSample else []
        newPlayersOnline: bool = newPlayersCheck(prevPlayers, players)

        log(f"({currentRecord.attempts}) [{currentRecord.time}] Online: {players} {'(New Players!!)' if newPlayersOnline else ''} | Ping: {currentRecord.ping}ms")
        currentRecord.playersOnline = ", ".join(players)

        return players

def checkingLoop(serverIP):
    server = JavaServer.lookup(serverIP)
    prevPlayers = []

    while True:
        currentRecord = Record()

        status = serverStatus(server, currentRecord)
        if status:
            prevPlayers = processStatusData(status, currentRecord, prevPlayers)

        writeRecord(currentRecord.recordAsList)

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
from threading import Thread
from win11toast import toast


def newPlayersCheck(oldList, newList) -> bool:
    newPlayers = [player for player in newList if player not in oldList]

    if newPlayers:
        notifThread = Thread(target=sendNotif, args=(newList, newPlayers), daemon=True)
        notifThread.start()
        return True
    else:
        return False

def sendNotif(allPlayers, newPlayers):
    nonNewPlayers = [player for player in allPlayers if player not in newPlayers]

    if nonNewPlayers:
        bodyMsg = f"Along with already playing players: {', '.join(nonNewPlayers)}"
    else:
        bodyMsg = "First one(s) online!"

    result = toast(
        f"{' + '.join(newPlayers)} joined!",
        bodyMsg,
        scenario="reminder",
        buttons=["Join", "Dismiss"]
    )

    if not isinstance(result, dict):
        return

    resultArgs: str = result.get("arguments", None)
    if not resultArgs:
        return

    if "join" in resultArgs.lower():
        openGame()

def openGame():
    print("Open game feature not implemented yet.")
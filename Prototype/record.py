from datetime import datetime

def timeAndDate() -> tuple:
    now = datetime.now()
    return now.strftime('%I:%M:%S %p'), now.strftime('%m-%d-%Y')

class Record:
    def __init__(self):
        self.time, self.date = timeAndDate()
        self.onlineStatus = None
        self.amountOnline = None
        self.playersOnline: str = None
        self.attempts = None
        self.ping = None
        self.error = None

    @property
    def recordAsList(self):
        return [
            self.time,
            self.date,
            self.onlineStatus,
            self.amountOnline,
            self.playersOnline,
            self.attempts,
            self.ping,
            self.error[:200] # Cap at 200
        ]
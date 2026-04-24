import gspread
from time import sleep

SERVICE_ACC_CREDS_PATH = "../Credentials/MC Status Checker Service Account.json"

def createGsServiceAcc():
    try:
        serviceAcc = gspread.service_account(SERVICE_ACC_CREDS_PATH)
        return serviceAcc

    except Exception as e:
        print(f"Could not carry out service account creation due to a(n) {type(e).__name__}: {e}.")

def openWorksheet(worksheetName):
    try:
        spreadsheet = gsServiceAcc.open("Server Status Checker")
        spreadWorksheet = spreadsheet.worksheet(worksheetName)

        return spreadWorksheet

    except Exception as e:
        print(f"Could not open worksheet due to a(n) {type(e).__name__}: {e}.")

def readData(columns: str):
    global worksheet

    attempts = 0

    while True:
        try:
            data = worksheet.get(columns)
            print(f"Got Data: {data}")

            return data

        except Exception as e:
            attempts += 1

            cooldown = min(2 ** attempts, 100)

            print(f"Could not carry out database read request due to a(n) {type(e).__name__}: {e}.\n"
                  f"Attempt #{attempts}.\n"
                  f"Retrying function after {cooldown} seconds.")

            sleep(cooldown)

def writeRecord(values: list[str, int]):
    global worksheet

    attempts = 0

    while True:
        try:
            worksheet.append_row(values)
            print(f"Appending row with values: '{values}'")
            return

        except Exception as e:
            attempts += 1

            cooldown = min(2 ** attempts, 100)

            print(f"Could not carry out database write request due to a(n) {type(e).__name__}: {e}.\n"
                  f"Attempt #{attempts}.\n"
                  f"Retrying function after {cooldown} seconds.")

            sleep(cooldown)

gsServiceAcc = createGsServiceAcc()
worksheet = openWorksheet("BMS SMP")
print("Startup: Opened Worksheet")
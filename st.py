import csv

# from collections import deque
import re


def is_number(s):
    pattern = r"^-?\d*\.?\d+$"
    return bool(re.match(pattern, s))


def start():
    FmcglRes = parseFmcglCSV()
    ExpRes = parseExpCSV()

    while True:
        startPrompt = str(input("Auto(A)/Manual(M): "))
        if startPrompt == "A":
            auto(FmcglRes, ExpRes)
            return
        elif startPrompt == "M":
            manual(FmcglRes, ExpRes)
            return


def parseFmcglCSV():
    # SKU on 1, count on 4
    with open("fmcgl.csv", newline="", encoding="utf-8", errors="ignore") as csvfile:
        reader = csv.reader(csvfile)

        fmcglDict = {}
        SKU = 1
        quantity = 4
        itemName = 3

        for row in reader:
            if not is_number(row[quantity]):
                continue
            fmcglDict[row[SKU]] = [row[itemName], int(row[quantity])]

        return fmcglDict


def parseExpCSV():
    # SKU on 8, count on 11
    with open("exp.csv", newline="", encoding="utf-8", errors="ignore") as csvfile:
        reader2 = csv.reader(csvfile)

        expDict = {}
        SKU = 8
        quantity = 11
        itemName = 1

        for row in reader2:
            if not is_number(row[quantity]):
                continue
            expDict[row[SKU]] = [row[itemName], int(row[quantity])]

        return expDict


def auto(fmcglDict, expDict):
    threshold = int(input("Threshold: "))

    transferArr = []
    for key, value in fmcglDict.items():
        if (
            expDict.get(key)
            and expDict.get(key)[1] is not None
            and expDict.get(key)[1] < 4
        ):
            item = fmcglDict.get(key)[0]
            fmcgl_quantity = value[1]
            exp_quantity = expDict.get(key)[1]
            transfer_quantity = threshold - exp_quantity
            itemSKU = key

            if transfer_quantity > fmcgl_quantity:
                transfer_quantity = fmcgl_quantity

            transferArr.append([itemSKU, item, transfer_quantity])
    print("SKU,Item,Qty")
    for i in transferArr:
        if i[2] < 1:
            continue
        print(i)

    return


def manual(fmcglDict, expDict):
    # Sku: [Name, Quantity]
    transferArr = []
    for key, value in fmcglDict.items():
        if (
            expDict.get(key)
            and expDict.get(key)[1] is not None
            and expDict.get(key)[1] < 4
        ):
            arr = []
            item = fmcglDict.get(key)[0]
            fmcgl_quantity = value[1]
            exp_quantity = expDict.get(key)[1]
            itemSKU = key

            while True:
                try:
                    print(f"\n{item}\nFMCGL: {fmcgl_quantity}\nExp: {exp_quantity}")
                    prompt = int(input("Transfer Qty: "))
                    if prompt <= fmcgl_quantity:
                        arr = [itemSKU, item, prompt]
                        transferArr.append(arr)
                        break
                    else:
                        input(
                            "\nERROR: Transfer qty exceeds qty available at FMCGL\nPress Enter to Try Again..."
                        )
                except ValueError:
                    input(
                        "\nERROR: Transfer Qty cannot be empty\nPress Enter to Try Again..."
                    )

    print("\nSKU,Item,Qty to send")
    for row in transferArr:
        if not row[2] < 1:
            print(f"{row[0]},{row[1]},{row[2]}")
    return


start()

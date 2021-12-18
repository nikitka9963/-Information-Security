import random


def erat():
    lst = []
    dct = {i: True for i in range(2, 2803)}

    i = 2
    while pow(i, 2) <= len(dct):
        if dct[i] is True:
            k = 1
            for j in range(pow(i, 2), len(dct), k * i):
                k += 1
                dct[j] = False
        i += 1

    for key, value in dct.items():
        if dct.get(key) is True:
            lst.append(key)

    return random.randint(lst[0], lst[len(lst) - 1])


def getSimDig():
    res = random.randint(2411, 2803)

    while not isPrime(res):
        res = random.randint(2411, 2803)

    return res


def isPrime(n):
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n and n % d != 0:
        d += 2
    return d * d > n


def genParKey(openKey1, closeKey, openKey2):
    return pow(openKey1, closeKey, openKey2)


def genFullKey(parKey, closeKey, openKey):
    return pow(parKey, closeKey, openKey)


def encryptMes(message, key):
    res = ""

    for let in message:
        res += chr(ord(let) + key)

    return res


def decipherMes(message, key):
    res = ""

    for let in message:
        res += chr(ord(let) - key)

    return res


if __name__ == '__main__':
    erat()
    mes = input("Введите сообщение : ")

    # Получение открытых и закрытых ключей на своих компьютерах
    aliceOpenKey = erat()
    aliceCloseKey = erat()
    bobOpenKey = erat()
    bobCloseKey = erat()

    print("p = " + str(aliceOpenKey) + "; g = " + str(bobOpenKey))

    # Получение частичных ключей
    aliceParKey = genParKey(aliceOpenKey, aliceCloseKey, bobOpenKey)
    print(f"A = {aliceOpenKey} ^ a mod {bobOpenKey} = {aliceParKey}")
    bobParKey = genParKey(aliceOpenKey, bobCloseKey, bobOpenKey)
    print(f"A = {aliceOpenKey} ^ b mod {bobOpenKey} = {bobParKey}")

    # Получение закрытого ключа для обмена сообщениями
    aliceFullKey = genFullKey(bobParKey, aliceCloseKey, bobOpenKey)
    print(f"s = {bobParKey} ^ a mod {bobOpenKey}")
    bobFullKey = genFullKey(aliceParKey, bobCloseKey, bobOpenKey)
    print(bobFullKey)
    print(aliceFullKey)
    print(f"s = {aliceParKey} ^ b mod {bobOpenKey}")
    print(f"s = {bobParKey} ^ a mod {bobOpenKey} = {aliceParKey} ^ b mod {bobOpenKey}")

    # Зашифровка сообщения
    mes = encryptMes(mes, aliceFullKey)
    print(mes)

    # Расшифровка сообщения
    print(decipherMes(mes, bobFullKey))



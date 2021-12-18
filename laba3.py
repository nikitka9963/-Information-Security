import random


def getSimDig(eil=None):
    if eil is None:
        dig = random.randint(13, 121)
        while not milRab(dig):
            dig = random.randint(13, 121)
    else:
        while 1:
            dig = random.randint(3, f - 1)
            while not milRab(dig):
                dig = random.randint(3, f - 1)

            if eil % dig != 0:
                break

    return dig


# Тест Миллера-Рабина
def milRab(n):
    s = 0
    num = n - 1

    while num % 2 == 0:
        num /= 2
        s += 1

    t = int((n - 1) / pow(2, s))

    for i in range(10):
        flag = False
        a = random.randint(2, n - 2)
        x = pow(a, t, n)

        if x == 1 or x == n - 1:
            continue

        for j in range(s - 1):
            x = pow(x, 2, n)

            if x == 1:
                return False

            if x == n - 1:
                flag = True
                break

        if not flag:
            return False
    return True


def getPrivKey(f, opExp):
    res = 3

    while res * opExp % f != 1:
        res += 1

    return res


def encryption(dig, exp, n1):
    return pow(dig, exp, n1)


def description(dig, d1, n1):
    return pow(dig, d1, n1)


mes = int(input("Введите сообщение : "))

# Получение простых чисел
p = getSimDig()
q = getSimDig()

# Получение модуля числа
n = p * q

if mes > n:
    print("error")

# Функция Эйлера
f = (p - 1) * (q - 1)

# Получение открытой экспоненты
opExp = getSimDig(f)

# Получение закрытого ключа
d = getPrivKey(f, opExp)

# Шифрование
mes = encryption(mes, opExp, n)
print(f"After encryption : {mes}")

# Дешифрование
print(f"After description : {description(mes, d, n)}")



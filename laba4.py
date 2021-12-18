import random
import sys

s = random.randint(1, 50)
a = random.randint(1, 50)
b = random.randint(1, 50)
I = random.randint(1, 50)


def hashLst(lst):
    sm = 0
    for el in lst:
        for ch in str(el):
            sm += ord(ch)
        sm += el * len(lst)

    return sm // len(lst)


def genN():
    q = random.randint(13, 121)
    N = 2 * q + 1

    while not milRab(q) and not milRab(N):
        q = random.randint(13, 121)
        N = 2 * q + 1

    return N


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


def getG(N):
    g = 2

    while not checkG(g, N):
        g += 1

    return g


def checkG(g, N):
    return pow(g, int((N - 1) / 2), N) + 1 == N


def checkValue(value):
    if value == 0:
        sys.exit()


N = genN()
g = getG(N)
k = hashLst([N, g])

p = int(input("Введите пароль : "))

x = hashLst([s, p])

v = pow(g, x, N)

A = pow(g, a, N)

B = (k * v + pow(g, b, N)) % N
checkValue(B)

u = hashLst([A, B])
checkValue(u)

Scl = pow(B - k * pow(g, x, N), (a + u * x)) % N

Kcl = hashLst([Scl])

Sserv = pow(A * pow(v, u, N), b) % N
Kserv = hashLst([Sserv])

Mcl = hashLst([hashLst([N]) ^ hashLst([g]), hashLst([I]), s, A, B, Kcl])
Mserv = hashLst([hashLst([N]) ^ hashLst([g]), hashLst([I]), s, A, B, Kserv])

if Mcl != Mserv:
    print("Mcl != Mserv")
    sys.exit()

Rcl = hashLst([A, Mcl, Kcl])
Rserv = hashLst([A, Mserv, Kserv])
if  Rcl != Rserv:
    print("wrong gen")
    sys.exit()

print(f"Mcl = {Mcl}; Mserv = {Mserv}; Rcl = {Rcl}; Rserv = {Rserv}")
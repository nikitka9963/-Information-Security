import operator
import re

alphabet = ['а', 'б', 'в', 'г', 'д',
            'е', 'ё', 'ж', 'з', 'и',
            'й', 'к', 'л', 'м', 'н',
            'о', 'п', 'р', 'с', 'т',
            'у', 'ф', 'х', 'ц', 'ч',
            'ш', 'щ', 'ъ', 'ы', 'ь',
            'э', 'ю', 'я']

frequency = {'о': 0.10983, 'е': 0.08483, 'а': 0.07998, 'и': 0.07367, 'н': 0.067,
             'т': 0.06318, 'с': 0.05473, 'р': 0.04746, 'в': 0.04533, 'л': 0.04343,
             'к': 0.03486, 'м': 0.03203, 'д': 0.02977, 'п': 0.02804, 'у': 0.02615,
             'я': 0.02001, 'ы': 0.01898, 'ь': 0.01735, 'г': 0.01687, 'з': 0.01641,
             'б': 0.01592, 'ч': 0.0145, 'й': 0.01208, 'х': 0.00966, 'ж': 0.0094,
             'ш': 0.00718, 'ю': 0.00639, 'ц': 0.00486, 'щ': 0.00361, 'э': 0.00331,
             'ф': 0.00267, 'ъ': 0.00037, 'ё': 0.00013}


def getNewText(excerpt):
    res = ""
    for let in excerpt.lower():
        if let == ' ' or let == "\n":
            res += let
            continue

        if not let.isalpha():
            continue

        res += let

    return res


def forEncr(n, word):
    while n > 32:
        n -= 32

    res = {}
    tmp = n

    for let in word:
        res[alphabet[tmp]] = let
        tmp += 1
        if tmp > 32:
            tmp = 0

    count = 0
    while count <= 32:
        if tmp > 32:
            tmp = 0

        if alphabet[count] not in res.values():
            res[alphabet[tmp]] = alphabet[count]
            count += 1
            tmp += 1
            continue

        count += 1

    return res


def encrypt(excerpt, alph):
    res = ""

    for let in excerpt:
        if let == " " or let == "\n":
            res += let
            continue

        res += alph[let]

    #inv_freq = {value: key for key, value in alph.items()}
    return res


def countAlph(excerpt):
    res = {}
    length = len(excerpt)
    for let in alphabet:
        count = len(re.findall(let, excerpt))
        res[let] = round(count / length, 5)

    return res


def nearest(target, lst):
    return min(lst, key=lambda x: abs(float(x) - target))


def frequencyAnalysis(excerpt, alphInTxt):
    inv_freq = {value: key for key, value in frequency.items()}
    for let in alphabet:
        ind = nearest(alphInTxt[let], list(frequency.values()))
        excerpt = excerpt.replace(let, inv_freq[ind])

    return excerpt


def getBigram(excerpt):
    excerpt = excerpt.replace(" ", "")
    length = len(excerpt)

    prev = excerpt[0]
    res = {}
    for cur in excerpt[1:]:
        key = ''.join(sorted(prev + cur))
        res[key] = res.get(key, 0) + 1
        prev = cur

    for key, value in res.items():
        res[key] = round(value / length, 5)

    return dict(sorted(res.items(), key=lambda x: x[1], reverse=True)[:10])


def getDict(excerpt, encrExcerpt):
    # Bigram
    encrExcerptBigram = getBigram(encrExcerpt)
    excerptBigram = getBigram(excerpt)
    res = {}
    res1 = {}

    i = 9
    for key in encrExcerptBigram.keys():
        res[key] = i
        i -= 1

    i = 9
    for key in excerptBigram.keys():
        res1[key] = i
        i -= 1

    # Monogram
    letInEncrEx = countAlph(encrExcerpt)
    sorted_tuples = sorted(letInEncrEx.items(), key=operator.itemgetter(1))
    letInEncrEx = {k: v for k, v in sorted_tuples}

    i = 0
    for key in letInEncrEx.keys():
        letInEncrEx[key] = str(i)
        i += 1

    letInEx = countAlph(excerpt)
    sorted_tuples = sorted(letInEx.items(), key=operator.itemgetter(1))
    letInEx = {k: v for k, v in sorted_tuples}

    i = 0
    for key in letInEx.keys():
        letInEx[key] = str(i)
        i += 1

    inv_letInEx = {value: key for key, value in letInEx.items()}
    for key, value in letInEncrEx.items():
        letInEncrEx[key] = inv_letInEx[value]

    return res, res1, letInEncrEx


def descryptWithBigram(bigramEncrDict, bigramDict, monogramDict, encrExcerpt):
    for key, value in bigramEncrDict.items():
        encrExcerpt = encrExcerpt.replace(key, str(value))

    print(encrExcerpt)

    encrExcerpt = encrExcerpt.translate(str.maketrans(monogramDict))

    for key, value in bigramDict.items():
        encrExcerpt = encrExcerpt.replace(str(value), key)

    return encrExcerpt


if __name__ == '__main__':
    with open("text.txt", "r", encoding='utf-8') as f:
        excerpt = f.read()

    excerpt = getNewText(excerpt)
    n = 561 #int(input("Шаг : "))
    word = "шифровка" #input("Слово : ")

    #Шифр цезаря с ключевым словом
    alph = forEncr(n, word)

    encrExcerpt = encrypt(excerpt, alph)

    print(f"После шифрования : \n{encrExcerpt}")

    #Расшифровка с помощью частотного анализа
    alphInTxt = countAlph(encrExcerpt)
    print(f"Расшифровка с помощью частотного анализа :\n{frequencyAnalysis(encrExcerpt, alphInTxt)}")

    #Расшифровка с помощью биграм
    bigramEncrDict, bigramDict, monogramDict = getDict(excerpt, encrExcerpt)
    print(f"Расшифровка с помощью биграмм и монограмм:\n{descryptWithBigram(bigramEncrDict, bigramDict, monogramDict, encrExcerpt)}")

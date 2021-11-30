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


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def encrypt(excerpt, step):
    res = ""
    for let in excerpt.lower():
        if let == ' ' or let == "\n":
            res += let
            continue

        ind = alphabet.index(let)
        ind = ind + step

        while ind > 32:
            ind = ind - 33

        while ind < 0:
            ind = 33 + ind

        res += alphabet[ind]

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
    length = len(excerpt)

    prev = excerpt[0]
    res = {}
    for cur in excerpt[1:]:
        key = ''.join(sorted(prev + cur))
        res[key] = res.get(key, 0) + 1
        prev = cur

    for key, value in res.items():
        res[key] = round(value / length, 5)

    return res


def descryptWithBigram(excerpt_new, bigramOld, bigramNew):
    for value in bigramNew.values():
        ind = nearest(value, list(bigramOld.values()))
        excerpt_new = excerpt_new.replace(get_key(bigramNew, value), get_key(bigramOld, ind))

    return excerpt_new


if __name__ == '__main__':
    with open("db.txt", "r", encoding='utf-8') as f:
        excerpt = f.read()

    excerpt = getNewText(excerpt)

    step = int(input("Введите шаг : "))

    excerpt_new = encrypt(excerpt, step)
    print(f"After encryption : \n {excerpt_new}")

    alphInTxt = countAlph(excerpt_new)

    print("After description with frequency analysis :\n" + frequencyAnalysis(excerpt_new, alphInTxt))

    excerptOldBigram = getBigram(excerpt)
    excerptNewBigram = getBigram(excerpt_new)

    print("After description with help of bigrams :\n" + descryptWithBigram(excerpt,
                                                                            excerptOldBigram,
                                                                            excerptNewBigram))

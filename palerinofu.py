def result(inp, outp, coded_text, frame='~'):
    print(frame * (len(inp) + 4))  # stringnél a szorzás ismétlést jelent
    print(f'# {inp} #')
    print(f'# BlackBox Magic > {"ˇ" * len(coded_text)} #')
    print(f'# {outp} #')
    print(frame * (len(inp) + 4))

def tesztelt_szoveg():
    text=input('Nosza írj be egy tesztelendő szöveget!')
    palerinofu(text)

def palerinofu(text):


    code_dict = {
        "p": "a",
        "l": "e",
        "r": "i",
        "n": "o",
        "f": "u",
        "k": "ö",
        "t": "é",
        "s": "ü",
    }

    coded_text = ""
    inp = 'Vizsgált szöveg: ' + text
    for char in text:
        # print(char)
        for code in code_dict:
            if char == code_dict[code]:
                # print(f'érték: {char} == {code_dict[code]} <-ezt # ere-> {code}')
                decode = code
                break
            elif char == code:
                # print(f'kulcs: {char} == {code} <-ezt # ere-> {code_dict[code]}')
                decode = code_dict[code]
                break
            else:
                # print(f'{char} változatlan marad (lefut az else) -> {char}')
                decode = char
        coded_text = coded_text + decode

    outp = '>>Kódolt szöveg: ' + coded_text
    result(inp, outp, coded_text)

    TryDeCod = input('Szeretnél egy ellenörző visszakódolást? (I / N)')
    answ = TryDeCod.upper()
    if answ == 'I':
        palerinofu(coded_text)

    exp_answ = ['I', 'N']
    while answ not in exp_answ:
        print(f'Nem megfelelő válasz "{TryDeCod}" ')
        TryDeCod = input('Lehetséges válasz: I vagy N:')
        answ = TryDeCod.upper()

        if answ == 'I':
            palerinofu(coded_text)

    else:
        print('Ok! A bizalom fontos! Hello!')
        exit()



tesztelt_szoveg()

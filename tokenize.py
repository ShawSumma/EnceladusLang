import string

operators = [
    '+', '-', '*', '/', '%', '^',
    '==', '!=', '<=', '>=', '>', "<",
    '||', '&&', '!'
    '+=', '-=', '*=', '/=', '%=', '~=', '=',
    '~', '<>', '=>', '->',
    ',', '?', ':'
]

opbegins = [i[0] for i in operators]


def tokenize(code):
    ret = []
    pl = 0
    maxpl = len(code)
    while pl < maxpl:
        cur = code[pl]
        if cur in '\t\r\n ':
            pl += 1
        elif cur == '"':
            tok = ''
            pl += 1
            cur = code[pl]
            while cur != '"':
                tok += cur
                pl += 1
                cur = code[pl]
            ret.append(['str', tok])
            pl += 1
        elif cur in string.ascii_letters or cur == '_':
            tok = ''
            while cur in string.ascii_letters or cur in "123456789_" and pl < maxpl:
                tok += cur
                pl += 1
                if pl >= maxpl:
                    break
                cur = code[pl]
            ret.append(['name', tok])
        elif cur in "0123456789":
            tok = ''
            while cur in "0123456789" and pl < maxpl:
                tok += cur
                pl += 1
                if pl >= maxpl:
                    break
                cur = code[pl]
            ret.append(['int', tok])
        elif cur in '({[':
            ret.append(['open', cur])
            pl += 1
        elif cur in ')}]':
            ret.append(['close', cur])
            pl += 1
        elif cur in opbegins:
            tok = cur
            pl += 1
            if tok + code[pl] in operators:
                tok += code[pl]
                pl += 1
            ret.append(['oper', tok])
    return ret

def main():
    return

if __name__ == '__main__':
    main()
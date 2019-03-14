
class Pair:
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

class Func:
    def __init__(self, place, argnames):
        self.place = place
        self.argnames = argnames

def fn_tostring(vals):
    ret = ""
    valsln = len(vals)
    pl = 0
    while pl < valsln:
        if pl != 0:
            ret += ' '
        cur = vals[pl]
        if isinstance(cur, int):
            ret += str(cur)
        elif isinstance(cur, str):
            ret += cur
        elif isinstance(cur, list):
            ret += '['
            ret += fn_tostring(cur)
            ret += ']'
        elif isinstance(cur, dict):
            ret += 'table('
            first = True
            for i in cur:
                if not first:
                    ret += ' '
                ret += fn_tostring([i]) + ' <> ' + fn_tostring([cur[i]])         
                first = False
            ret += ')'
        elif isinstance(cur, Pair):
            ret += fn_tostring([cur.car]) + ' <> ' + fn_tostring([cur.cdr])
        elif isinstance(cur, Func):
            ret += "<func at " + str(cur.place) + ">"     
        else:
            print('error')
            print('string type error')
            exit(1)
        pl += 1
    return ret

def fn_table(vals):
    ret = {}
    for i in vals:
        ret[i.car] = i.cdr
    return ret

def fn_print(vals):
    print(fn_tostring(vals))

def op_add(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a + b
    print('error')
    print('can only + numbers')
    exit(1)

def op_sub(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a - b
    print('error')
    print('can only - numbers')
    exit(1)

def op_mul(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a * b
    print('error')
    print('can only * numbers')
    exit(1)

def op_div(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a / b
    print('error')
    print('can only / numbers')
    exit(1)

def op_cat(a, b):
    if isinstance(a, list) and isinstance(b, list):
        return a + b
    if isinstance(a, dict) and isinstance(b, dict):
        return {**a, **b}
    print('error')
    print('can only ++ vectors')
    exit(1)

def op_pair(a, b):
    return Pair(a, b)

def op_at(a, b):
    return a[b]

names = {
    'print': fn_print,
    'table': fn_table,
}

names = [names]

opers = {
    '+': op_add,
    '-': op_sub,
    '*': op_mul,
    '/': op_div,
    '<': lambda x, y: x < y,
    '>': lambda x, y: x > y,
    '<=': lambda x, y: x <= y,
    '>=': lambda x, y: x >= y,
    '==': lambda x, y: x == y,
    '!=': lambda x, y: x != y,
    '~': op_cat,
    '->': op_at,
    '<>': op_pair,
    ':': lambda x, y: [x, y],
    '?': lambda x, y: x[0] if y else x[1]
}

def byterun(code):
    place = 0
    codeln = len(code)
    stack = []
    retstack = []
    while place < codeln:
        cur = code[place]
        if cur[0] == 'push':
            stack.append(cur[1])
        elif cur[0] == 'pop':
            stack.pop()
        elif cur[0] == 'list' or cur[0] == 'tuple':
            ls = []
            for i in range(cur[1]):
                ind = -(cur[1] - i)
                ls.append(stack[ind])
            for i in range(cur[1]):
                stack.pop()
            stack.append(ls)
        elif cur[0] == 'ret':
            names.pop()
            place = retstack[-1]
            retstack.pop()
        elif cur[0] == 'call':
            ls = []
            args = stack[-1]
            stack.pop()
            func = stack[-1]
            stack.pop()
            if callable(func):
                stack.append(func(args))
            else:
                names.append({})
                for k, v in zip(func.argnames, args):
                    names[-1][k] = v
                retstack.append(place)
                place = func.place
        elif cur[0] == 'load':
            for i in names[::-1]:
                if cur[1] in i:
                    stack.append(i[cur[1]])
                    break
            else:
                print('error')
                print('cant load name', cur[1])
                exit(1)
        elif cur[0] == 'binop':
            rhs = stack[-1]
            stack.pop()
            lhs = stack[-1]
            got = opers[cur[1]](lhs, rhs)
            stack[-1] = got
        elif cur[0] == 'store':
            names[-1][cur[1]] = stack[-1]
        elif cur[0] == 'fn-jump':
            fn = Func(place, stack[-1])
            stack[-1] = fn
            place += cur[1]
        else:
            print('error')
            print(cur)
            exit(1)
        place += 1
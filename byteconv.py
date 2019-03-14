def conv(ast):
    asttype = ast[0]        
    if asttype == 'call':
        ret = []
        ret += conv(ast[1])
        args = ast[2]
        if args[0] == 'paren':
            for i in args[1]:
                ret += conv(i)
            ret.append(['list', len(args[1])])
            ret.append(['call'])
        elif args[0] == 'square':
            ret += conv(args[1])
            ret.append(['index', count])
        return ret
    elif asttype == 'square':
        ret = []
        for i in ast[1]:
            ret += conv(i)
        ret.append(['list', len(ast[1])])
        return ret
    elif asttype == 'paren' or asttype == 'curly':
        ret = []
        count = len(ast[1])
        for i in ast[1]:
            ret += conv(i)
            ret.append(['pop'])
        ret.pop()
        return ret
    elif asttype == 'str':
        ret = []
        ret.append(['push', ast[1]])
        return ret
    elif asttype == 'name':
        ret = []
        ret.append(['load', ast[1]])
        return ret
    elif asttype == 'int':
        ret = []
        ret.append(['push', int(ast[1])])
        return ret
    elif isinstance(asttype, list) and len(asttype) == 2 and asttype[0] == 'oper':
        optype = asttype[1]

        if optype == '=':
            ret = []
            lhs = ast[1]
            rhs = ast[2]
            if lhs[0] == 'call':
                name = lhs[1][1]
                args = lhs[2][1]
                body = conv(rhs)
                ret.append(['push', [i[1] for i in args]])
                ret.append(['fn-jump', len(body)+1])
                ret += body
                ret.append(['ret'])
                ret.append(['store', name])
            else:
                ret += conv(rhs)
                ret.append(['store', lhs[1]])
            return ret
        elif optype == '=>':
            ret = []
            argl = ast[1]
            body = ast[2]
            body = conv(body)
            if argl[0] == 'name':
                argl = [argl[1]]
            else:
                argl = [i[1] for i in argl[1]]
            ret.append(['push', argl])
            ret.append(['fn-jump', len(body)+1])
            ret += body
            ret.append(['ret'])
            return ret
        elif optype == ':':
            ret = []
            for side in ast[1:]:
                body = conv(side)
                ret.append(['push', []])
                ret.append(['fn-jump', len(body)+1])
                ret += body
                ret.append(['ret'])
            ret.append(['binop', ':'])
            return ret
        elif optype == '?':
            ret = []
            ret += conv(ast[2])
            ret += conv(ast[1])
            ret.append(['binop', '?'])
            ret.append(['list', 0])
            ret.append(['call'])
            return ret
        ret = []
        ret += conv(ast[1])
        ret += conv(ast[2])
        ret.append(['binop', optype])
        return ret
    print('error in ast')
    print(ast)
    exit(1)

def byteconv(ast):
    ret = []
    for i in ast:
        ret += conv(i)
    return ret
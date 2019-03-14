def strdump(opcodes):
    ret = []
    for i in opcodes:
        optype = i[0]
        if optype == 'push':
            if isinstance(i[1], int):
                ret.append('int ' + str(i[1]))
            if isinstance(i[1], str):
                ret.append('str ' + i[1])
            if isinstance(i[1], list):
                ret.append('names '+ ', '.join(i[1]))
        elif optype == 'call':
            ret.append('call')
        elif optype == 'list':
            ret.append('list ' + str(i[1]))
        elif optype == 'store':
            ret.append('store ' + str(i[1]))
        elif optype == 'fn-jump':
            ret.append('fn ' + str(i[1]))
        elif optype == 'load':
            ret.append('load ' + i[1])
        elif optype == 'binop':
            ret.append('binop ' + i[1])
        elif optype == 'ret':
            ret.append('ret')
        else:
            print(i)
    return '\n'.join(ret)
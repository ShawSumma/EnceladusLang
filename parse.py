import util
import tokenize

def pair(lis, left, right, maxdepth=0):
    return multi_pair(lis, [left], [right], maxdepth)

def multi_pair(lis, lefts, rights, maxdepth=0):
    ret = {}
    hold = []
    depth = 0
    for pl, i in enumerate(lis):
        for left in lefts:
            if i == left:
                depth += 1
                hold.append(pl)
                break
        for right in rights:
            if i == right:
                if maxdepth == 0 or depth < maxdepth:
                    ret[hold[-1]] = pl
                hold.pop()
                depth -= 1
                break
    return ret

def merge_upon_func(lis, merge, call=list, left=True):
    if not left:
        lis = lis[::-1]
    ret = []
    donext = True
    for i in lis:
        if merge(i):
            ret[-1] = call([i, None, ret[-1]])
            donext = False
        elif not donext:
            ret[-1][1] = i
            donext = True
        else:
            ret.append(i)
    if not left:
        ret = ret[::-1]
    return ret

def split(lis, when):
    ret = [[]]
    for i in lis:
        if i == when:
            if len(ret[-1]) != 0:
                ret.append([])
        else:
            ret[-1].append(i)
    return ret

def multi_merge_upon(lis, merges, call=list, left=True):
    return merge_upon_func(
        lis,
        lambda i: i in merges,
        call,
        left
    )

def merge_upon(lis, merge, call=list, left=True):
    return multi_merge_upon(lis, [merge], call, left)

def paren_parse(tokens):
    pairs = multi_pair(
        tokens,
        [
            ['open', '('],
            ['open', '{'],
            ['open', '['],
        ],
        [
            ['close', ')'],
            ['close', '}'],
            ['close', ']'],
        ]
    )

    subkinds = {
        '(': 'paren',
        '{': 'curly',
        '[': 'square',
    }

    ret = []
    pl = 0
    maxpl = len(tokens)
    while pl < maxpl:
        if pl in pairs:
            typesub = subkinds[tokens[pl][1]]
            endpl = pairs[pl]
            sub = tokens[pl+1:endpl]
            sub = parse_tokens(sub)
            ret.append([typesub, sub])
            pl = endpl
        else:
            ret.append(tokens[pl])
        pl += 1
    return ret

def call_parse(tokens):
    ret = []
    kindsof = ['paren', 'curly']
    for token in tokens:
        if len(ret) > 0 and ret[-1][0] != 'oper' and token[0] in kindsof:
            ret[-1] = ['call', ret[-1], token] 
        else:
            ret.append(token)
    return ret

def parse_tokens(tokens):
    tokens = paren_parse(tokens)
    tokens = call_parse(tokens)
    oper_order = [
        ['->'],
        ['<>', '~'],
        ['*', '/', '%'],
        ['+', '-'],
        ['>', '>=', '<', '<='],
        ['!=', '=='],
        ['&&', '||'],
        [':', '?'],
        ['+=', '-=', '*=', '/=', '%=', '='],
        ['=>']
    ]
    spl = tokens
    for lvl in oper_order:
        merge_check = [['oper', i] for i in lvl]
        spl = multi_merge_upon(spl, merge_check, left=False)
    return spl

def parse(code):
    ret = parse_tokens(tokenize.tokenize(code))
    return ret

def main():
    return

if __name__ == '__main__':
    main()
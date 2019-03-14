import util
import parse
import byteconv
import bytedump
import backend.interp as interp

ast = parse.parse(util.slurp('main.tach'))
opcodes = byteconv.byteconv(ast)
fil = open('cache/out.txt', 'w')
fil.write(bytedump.strdump(opcodes))
fil.close()
interp.byterun(opcodes)
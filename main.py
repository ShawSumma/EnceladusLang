import util
import parse
import byteconv
import interp

ast = parse.parse(util.slurp('main.tach'))
opcodes = byteconv.byteconv(ast)
interp.byterun(opcodes)
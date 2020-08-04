import sys
import parser2
import interp2

data = open('D:/laba2/robot').read()
prog = parser2.parse(data)
if not prog:
    raise SystemExit
b = interp2.Interp(prog)
try:
    b.run()
    raise SystemExit
except RuntimeError:
    pass

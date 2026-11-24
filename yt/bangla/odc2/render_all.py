import sys, asyncio
from boards import build
from engine import render_board
names = sys.argv[1:]
for b in build():
    if b.name in names:
        asyncio.run(render_board(b))

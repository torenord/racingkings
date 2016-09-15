from position import Position
from search import negamaxpos
import readline
import sys
import time

# Initial game position
position = Position().setup()

def decode(s):
    x = ord(s[0]) - ord("a")
    y = 8 - int(s[1])

    return x, y

def handle(cmd):
    global position

    # Quit
    if cmd == "q":
        exit()

    # Help
    if cmd == "h":
        print("q -- Quit")
        print("h -- Help")
        print("p -- Print current position")
        print("l -- Load position from file")
        print("s -- Save position from file")
        print("n -- Print legal next positions")
        print("c -- Compute and apply next positions")
        print("m -- Move a piece")

    # Print current position
    elif cmd == "p":
        print(position)

    # Load position from file
    elif cmd.split(" ")[0] == "l":
        try:
            filename = cmd.split(" ")[1]
            position = Position().parse(open(filename).read())
            print(position)
        except (IndexError, ValueError):
            pass

    # Save position from file
    elif cmd.split(" ")[0] == "s":
        try:
            filename = cmd.split(" ")[1]
            with open(filename, "w") as f:
                f.write(repr(position))
        except (IndexError, ValueError):
            pass

    # Print legal next positions
    elif cmd == "n":
        for p in position.legalmoves():
            print(p)

    # Move a piece
    elif cmd.split(" ")[0] == "m":
        a = cmd.split(" ")[1]
        b = cmd.split(" ")[2]

        y1, x1 = decode(a)
        y2, x2 = decode(b)

        position.movepiece(x1, y1, x2, y2)
        position.whitesTurn = not position.whitesTurn
        print(position)

    # Compute and apply next positions
    elif cmd.split(" ")[0] == "c":
        try:
            start = time.time()
            depth = int(cmd.split(" ")[1])
            p = negamaxpos(position, depth, -1000, 1000)
            print(p)
            position = p
            end = time.time()
            print("Completed in {0:.3} seconds.".format(end - start))
        except (IndexError, ValueError):
            pass

if len(sys.argv) == 2:
    handle(sys.argv[1])
else:
    while True:
        try:
            cmd = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        handle(cmd)

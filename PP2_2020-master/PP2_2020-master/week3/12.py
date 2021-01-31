# json.dump
# json.load

import json
# d = {"AAA": 23, "BBB": 10, "CCC": 34}

# with open("game.txt", "w") as f:
#     json.dump(d, f)

with open("game.txt", "r") as f:
    d = json.load(f)
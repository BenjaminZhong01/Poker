NUM_SEATS_PER_TABLE = 10

# User status
READY = 1
NOTREADY = 0

# Game rounds
ROUND = [0, 1, 2, 3] # "preflop", "flop", "turn", "river"

# Role
ROLE = [-1, 0, 1, 2] # -1: no role, 0: dealer, 1: small blind, 2: big blind


# Button Available
BUTTON = [0, 1, 2, 3, 4, 5, 6] # 0: no buttons available, 1: only raise to 5 available, 2: only raise to 10 available, 3: call+raise+fold, 4: check+raise, 5: allin, 6: folded
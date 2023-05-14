from tqdm import tqdm

from main import main

X_WON = 1
O_WON = 2
DRAW = 0


def run_and_get_result(x_depth, o_depth):
    cmd = ["--no-display",
           "--x-depth={}".format(x_depth), "--o-depth={}".format(o_depth)]
    winner = main(cmd)
    if winner == "x":
        return X_WON
    elif winner == "o":
        return O_WON
    else:
        return DRAW


run_configs = [
    (4, 4, 1000)
]

for config in run_configs:
    (x_depth, o_depth, runs) = config

    x_won = 0
    o_won = 0
    draw = 0
    for i in tqdm(range(runs)):
        # print("Running Game ... {}".format(i+1))
        r = run_and_get_result(x_depth, o_depth)
        if r == DRAW:
            draw += 1
        elif r == X_WON:
            x_won += 1
        elif r == O_WON:
            o_won += 1
        # print("Game Ended")

    print("x: {}, o: {}, draw: {}".format(x_won / (1.0 * runs),
          o_won / (1.0 * runs), draw / (1.0 * runs)))

from operator import itemgetter

tiles = [
    [3, "A"],
    [4, "A"],
    [5, "A"],
    [6, "A"],
    [7, "A"],

    [6, "B"],
    [6, "C"],
    [6, "A"],
    [6, "D"],

    [6, "A"],
    [6, "B"],
    [6, "D"],

    [1, "B"],
    [2, "B"],
    [3, "B"],
    [7, "B"],
    [7, "C"],
    [10, "D"],
    [11, "C"],
    [12, "D"]
]

def groups_try(suit,lefts, all_combinations):
    sub_results = []
    subsuit = suit[:]
    leftscopy = lefts[:]
    if (len(all_combinations) > 1):
        if lefts == all_combinations[-2][-1]:
            suit = []
            return
    for i, tile0 in enumerate(leftscopy):
        sub_results.append(tile0)
        for tile1 in leftscopy[i+1:]:
            # ----Here code is included to use jockers.
            if (tile1[0] == sub_results[-1][0]) and (tile1 not in sub_results) and tile0[1] != tile1[1]:
                sub_results.append(tile1)
                if len(sub_results) >= 3:
                    cards_left = leftscopy[:]
                    for tile in sub_results:
                        cards_left.remove(tile)
                    all_combinations.append([suit[:] + sub_results[:], list(cards_left)])
                    groups_try(suit[:] + sub_results[:],cards_left[:],all_combinations)
        sub_results = []
    return subsuit,leftscopy

def runs_try(all_combinations):
    run = []
    for i, combination in enumerate(all_combinations):
        hand, tiles = combination
        if (len(tiles) == 0):
            return [combination]
        for index, tile0 in enumerate(tiles):
            run.append(tile0)
            for tile1 in tiles[index+1:]:
                if (tile1[0] == run[-1][0] + 1) and (tile0[1] == tile1[1] or tile1[1] == "jocker"):
                    run.append(tile1)
                    if len(run) >= 3:
                        cards_left = tiles[:]
                        for tilex in run:
                            cards_left.remove(tilex)
                        if (len(cards_left) == 0):
                            return [[[list(run) + list(hand), cards_left], 0]]
                        if (not(sorted(all_combinations[-1][-1]) == sorted(cards_left))):
                            all_combinations.append(
                                [list(run) + list(hand), cards_left])
                            runs_try(all_combinations[i+1:])

            run = []

    return all_combinations

def play(tiles):
    first_combinations = [[[], tiles]]
    output_runs_combination = runs_try(first_combinations)
    all_combinations = []
    if(len(output_runs_combination) == 1):
        return output_runs_combination[0]
    for runs_combination in output_runs_combination[1:]:
        groups_try(runs_combination[0],runs_combination[1], all_combinations)
    new_combinations = []
    for combination in reversed(all_combinations):
        hand, cards_left = combination
        score = 0
        for card in cards_left:
            score += card[0]
        new_combinations.append([list(hand), list(cards_left), score])

    sorted_combinations = sorted(new_combinations, key=itemgetter(2))
    return sorted_combinations

print(play(tiles)[0])
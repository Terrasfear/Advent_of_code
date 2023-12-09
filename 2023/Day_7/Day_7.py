import numpy as np


# hashing functions
def card_value(card: str):
    if card.isdigit():
        return "0" + card
    else:  # i.e. A, K, Q, J or T
        if card == "A":
            return "14"
        if card == "K":
            return "13"
        if card == "Q":
            return "12"
        if card == "J":
            return "11"
        if card == "T":
            return "10"


def card_value_joker(card: str):
    if card.isdigit():
        return "0" + card
    else:  # i.e. A, K, Q, J or T
        if card == "A":
            return "13"
        if card == "K":
            return "12"
        if card == "Q":
            return "11"
        if card == "T":
            return "10"
        if card == "J":
            return "01"


def hand_rank(hand: str):
    num_per_face = {"A": 0,
                    "K": 0,
                    "Q": 0,
                    "J": 0,
                    "T": 0,
                    "9": 0,
                    "8": 0,
                    "7": 0,
                    "6": 0,
                    "5": 0,
                    "4": 0,
                    "3": 0,
                    "2": 0}

    for card in hand:
        num_per_face[card] += 1

    num_values = list(num_per_face.values())

    if 5 in num_values:  # 5 of a kind
        # print("5 of a kind",end="\t\t")
        return "7"
    if 4 in num_values:  # 4 of a kind
        # print("4 of kind",end="\t\t")
        return "6"
    if 2 in num_values and 3 in num_values:  # full house
        # print("full house",end='\t\t')
        return "5"
    if 3 in num_values:  # 3 of a kind
        # print("3 of a kind", end='\t\t')
        return "4"
    if num_values.count(2) == 2:  # two pair
        # print("2 pair", end='\t\t\t')
        return "3"
    if num_values.count(2) == 1:  # one pair
        # print("1 pair", end='\t\t\t')
        return "2"

    # print("high card", end='\t\t')
    return "1"  # high card


def hand_rank_joker(hand):
    num_per_face = {"A": 0,
                    "K": 0,
                    "Q": 0,
                    "T": 0,
                    "9": 0,
                    "8": 0,
                    "7": 0,
                    "6": 0,
                    "5": 0,
                    "4": 0,
                    "3": 0,
                    "2": 0,
                    "J": 0}

    for card in hand:
        num_per_face[card] += 1

    num_values_sans_J = list(num_per_face.values())[0:-1]

    if max(num_values_sans_J) + num_per_face["J"] >= 5:  # 5 of a kind
        # print("5 of a kind",end="\t\t")
        return "7"

    if max(num_values_sans_J) + num_per_face["J"] >= 4:  # 4 of a kind
        # print("4 of kind",end="\t\t")
        return "6"

    if 2 in num_values_sans_J and 3 in num_values_sans_J:  # full house
        # print("full house",end='\t\t')
        return "5"
    if num_values_sans_J.count(2) == 2 and num_per_face["J"] == 1:  # full house with joker
        return "5"

    if max(num_values_sans_J) + num_per_face["J"] >= 3:  # 3 of a kind
        # print("3 of a kind", end='\t\t')
        return "4"

    if num_values_sans_J.count(2) == 2:  # two pair
        # print("2 pair", end='\t\t\t')
        return "3"

    if max(num_values_sans_J) + num_per_face["J"] >= 2:  # one pair
        # print("1 pair", end='\t\t\t')
        return "2"

    # print("high card", end='\t\t')
    return "1"  # high card


def hand_hash(hand: str):
    hash_value = int(hand_rank(hand) + "".join([card_value(card) for card in hand]))
    # print(hash_value)
    return hash_value


def hand_hash_joker(hand: str):
    hash_value = int(hand_rank_joker(hand) + "".join([card_value_joker(card) for card in hand]))
    # print(hash_value)
    return hash_value


_file = open("input", 'r')
_lines = _file.readlines()

_game = [{"hand": "zzzzz",
          "hash": 99999999999,
          "hash_j": 99999999999,
          "bid": 1000,
          "rank": len(_lines),
          "rank_j": len(_lines)} for _ in range(len(_lines))]

# generate hands list with hash
for _idx, _line in enumerate(_lines):
    _hand, _bid = _line.split()

    _game[_idx]["hand"] = _hand
    _game[_idx]["hash"] = hand_hash(_hand)
    _game[_idx]["hash_j"] = hand_hash_joker(_hand)
    _game[_idx]["bid"] = int(_bid)

# generate ranks

_ordered_indices = np.argsort([_hand["hash"] for _hand in _game])
_ordered_indices_j = np.argsort([_hand["hash_j"] for _hand in _game])

# part 1
_winnings = 0
_rank = 1
# compute winnings
for _idx in _ordered_indices:
    _hand = _game[_idx]

    _hand["rank"] = _rank

    _winnings += _rank * _hand["bid"]
    _rank += 1

    # print(f"{_hand['hand']}\t{_hand['hash']}\t{_hand['rank']}\t{_hand['bid']}")


# part 2
_winnings_j = 0
_rank_j = 1
# compute winnings
for _idx_j in _ordered_indices_j:
    _hand = _game[_idx_j]

    _hand["rank_j"] = _rank_j

    _winnings_j += _rank_j * _hand["bid"]
    _rank_j += 1

    print(f"{_hand['hand']}\t{str(_hand['hash_j'])[0]}\t{_hand['rank_j']}\t{_hand['bid']}")
    # print(f"{_hand['hand']}\t{_hand['hash_j']}\t{_hand['rank_j']}\t{_hand['bid']}\t{_hand['hash']}\t{_hand['rank']}")


print(f"Part 1: {_winnings}")
print(f"Part 2: {_winnings_j}")

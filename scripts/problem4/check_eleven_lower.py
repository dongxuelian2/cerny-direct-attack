"""Independent literal thirteen-state lower witness; all short words, no cache."""
from itertools import product


ROWS = (
    (0, 1, 2, 3, 5, 4, 7, 8, 9, 10, 11, 12, 6),
    (9, 0, 1, 2, 3, 4, 7, 8, 5, 10, 11, 5, 12),
)
Q = frozenset(range(13))
S = frozenset(range(9))


def image(states, word):
    for letter in word:
        states = frozenset(ROWS[letter][q] for q in states)
    return states


def main():
    # Every state reaches every other state using the literal transition table.
    for start in Q:
        seen = {start}
        todo = [start]
        for q in todo:
            for row in ROWS:
                if row[q] not in seen:
                    seen.add(row[q])
                    todo.append(row[q])
        assert seen == Q
    reaching = (1,) * 3 + ((0,) * 6 + (1,) * 9) * 3 + (0,) * 4
    assert image(Q, reaching) == S

    # A direct word tree checks every word, including duplicate subset images.
    safe_counts = []
    for length in range(12):
        safe = sum(len(out := image(S, word)) == 9 and 0 in out
                   for word in product(range(2), repeat=length))
        safe_counts.append(safe)
        if length < 11:
            assert safe == 2 ** length
        else:
            assert safe < 2 ** length
    attaining = (0,) * 6 + (1,) + (0,) * 3 + (1,)
    assert len(image(S, attaining)) == 8

    # Synchronization is verified by explicitly merging pairs in the current
    # image; the reference uses set-valued transitions and records real words.
    current, reset = Q, ()
    while len(current) > 1:
        pair = frozenset(sorted(current)[:2])
        todo, words = [pair], {pair: ()}
        for pair in todo:
            if len(pair) == 1:
                merging = words[pair]
                break
            for letter in range(2):
                out = image(pair, (letter,))
                if out not in words:
                    words[out] = words[pair] + (letter,)
                    todo.append(out)
        else:
            raise AssertionError("a pair does not merge")
        current = image(current, merging)
        reset += merging
    assert len(image(Q, reset)) == 1
    print("PASS: literal rows are strongly connected and synchronizing; Qv=S.")
    print("All 4095 words of length 0..11 checked; safe counts:", safe_counts)
    print("Exact ac(S,{0})=11; aaaaaabaaab compresses to eight states.")


if __name__ == "__main__":
    main()

"""Reconstruct small automata and compare native scores with independent set BFS."""
from itertools import product
import random
from direct_attack.check_new_image_results import distances
from direct_attack.core import strongly_connected
from direct_attack.native_policy import profile


def cases():
    for values in product(range(3), repeat=6):
        yield [list(values[:3]), list(values[3:])]
    rng = random.Random(130901)
    for _ in range(128):
        n = rng.randrange(3, 7)
        yield [[rng.randrange(n) for _ in range(n)] for _ in range(2)]


def main():
    tested = checked = nonsync = 0
    for rows in cases():
        tested += 1
        if not strongly_connected(rows):
            continue
        actual = profile(rows, details=True)
        if actual is None:
            nonsync += 1
            continue
        _, forward, _, extension, best, _, worst = distances(rows, with_worst=True)
        encode = lambda S: sum(1 << q for q in S)
        assert actual['extension'] == {encode(S): v for S, v in extension.items()}
        assert actual['best'] == {encode(S): v for S, v in best.items()}
        assert actual['worst'] == {encode(S): v for S, v in worst.items()}
        assert actual['rt'] == min(v for S, v in forward.items() if len(S) == 1)
        checked += 1
    assert tested == 857 and checked > 0 and nonsync > 0
    print(f'PASS: {tested} generated automata; {checked} native/set-BFS comparisons; {nonsync} nonsynchronizing controls')


if __name__=='__main__':main()

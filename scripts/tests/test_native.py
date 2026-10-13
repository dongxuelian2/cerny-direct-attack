"""Differential controls for the new C++ implementation, not proof verification."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import itertools
import random
import subprocess
import unittest

from automata.engine import forward_distance
from scripts.problem4.verify_certificates import ac
from run import ROOT, compile_cpp


class NativeSearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.exe = compile_cpp(ROOT/'scripts/native/subset_search.cpp')

    def run_cases(self, records, threads):
        out = subprocess.run([str(self.exe), '--threads', str(threads)], input='\n'.join(records)+'\n',
                             text=True, capture_output=True, check=True)
        return [list(map(int, line.split())) for line in out.stdout.splitlines()]

    def test_all_binary_three_state_automata_and_thread_order(self):
        records, expected, rows_list = [], [], []
        for values in itertools.product(range(3), repeat=6):
            rows = [list(values[:3]), list(values[3:])]
            a = dict(n=3, letters=['a', 'b'], transitions=rows)
            expected.append(forward_distance(a))
            records.append('reset 3 2 '+' '.join(map(str, values)))
            rows_list.append(rows)
        one = self.run_cases(records, 1)
        many = self.run_cases(records, 4)
        self.assertEqual(one, many)
        self.assertEqual(len(one), 729)
        for result, target, rows in zip(one, expected, rows_list):
            length, _, *word = result
            self.assertEqual(length, -1 if target is None else target)
            if length >= 0:
                states = set(range(3))
                for letter in word: states = {rows[letter][q] for q in states}
                self.assertEqual(len(states), 1)
                self.assertEqual(len(word), length)

    def test_random_avoid_or_compress_instances(self):
        rng = random.Random(130901)
        records, expected, cases = [], [], []
        for _ in range(128):
            n = rng.randrange(3, 9)
            rows = [[rng.randrange(n) for _ in range(n)] for _ in range(2)]
            S = set(rng.sample(range(n), rng.randrange(2, n+1)))
            A = set(rng.sample(sorted(S), rng.randrange(1, len(S))))
            mask = lambda xs: sum(1 << q for q in xs)
            records.append(f'avoid {n} 2 {mask(S)} {mask(A)} '+' '.join(str(q) for row in rows for q in row))
            expected.append(ac(rows, S, A))
            cases.append((rows, S, A))
        answers = self.run_cases(records, 4)
        self.assertEqual(len(answers), len(records))
        for answer, target, (rows, S, A) in zip(answers, expected, cases):
            length, _, *word = answer
            self.assertEqual(length, -1 if target is None else target)
            if length >= 0:
                end = set(S)
                for letter in word: end = {rows[letter][q] for q in end}
                self.assertTrue(len(end) < len(S) or not A <= end)
                self.assertEqual(len(word), length)

    def test_rejects_truncated_and_out_of_domain_inputs(self):
        for record in ('reset 3 2 0 1', 'reset 25 1', 'reset 2 1 0 2', 'avoid 3 1 3 3 0 1 2'):
            result = subprocess.run([str(self.exe)], input=record, text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()

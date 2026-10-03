"""Run from project root: python -m unittest discover -s tests -v"""
from __future__ import annotations
import copy
import itertools
import random
import unittest
from src.engine import cerny, exact, abstract, FEATURES, forward_distance, SEED, landmark_experiment
from src.check_certificate import check, CertificateError

class LabTests(unittest.TestCase):
    def test_cerny_2_through_10(self):
        for n in range(2,11):
            cert=exact(cerny(n))
            self.assertEqual(cert['lower_bound'],(n-1)**2)
            self.assertEqual(forward_distance(cerny(n)),(n-1)**2)
            self.assertTrue(check(cert)['verified'])
    def test_all_729_binary_three_state_automata(self):
        for v in itertools.product(range(3),repeat=6):
            a={'n':3,'letters':['a','b'],'transitions':[list(v[:3]),list(v[3:])]}
            cert=exact(a);reference=forward_distance(a)
            self.assertTrue(check(cert)['verified'])
            self.assertEqual(cert.get('upper_bound'),reference)
    def test_128_random_cases(self):
        rng=random.Random(SEED)
        for _ in range(128):
            n=rng.randint(2,8)
            a={'n':n,'letters':['a','b'],'transitions':[[rng.randrange(n) for _ in range(n)] for _ in range(2)]}
            cert=exact(a)
            self.assertEqual(cert.get('upper_bound'),forward_distance(a))
            self.assertTrue(check(cert)['verified'])
    def test_features_and_cardinality_obstruction(self):
        for n in range(3,9):
            ex=exact(cerny(n))
            for mode in FEATURES:
                cert,row=abstract(cerny(n),mode,ex)
                self.assertTrue(check(cert)['verified'])
                self.assertLessEqual(cert['lower_bound'],(n-1)**2)
                if mode=='identity':self.assertEqual(cert['lower_bound'],(n-1)**2)
                if mode=='cardinality':self.assertEqual(cert['lower_bound'],n-1)
    def test_marked_closed_form_every_subset(self):
        for n in range(3,11):
            cert,_=abstract(cerny(n),'marked')
            for mask in range(1,1<<n):
                k=mask.bit_count();u=mask&1;v=mask>>(n-1)&1
                predicted=0 if k==1 else (3*k-3 if v==0 else (3*k-4 if u==0 else 3*k-5))
                self.assertEqual(cert['potential'][mask],predicted)
    def test_landmark_refinement_and_full_information(self):
        for n in range(3,9):
            bounds=[]
            for r in range(n+1):
                cert,_=landmark_experiment(cerny(n),r)
                self.assertTrue(check(cert)['verified']);bounds.append(cert['lower_bound'])
            self.assertEqual(bounds,sorted(bounds))
            self.assertEqual(bounds[n-1],(n-1)**2)
    def test_reject_wrong_local_bound(self):
        c=exact(cerny(4));c['potential'][-1]+=1;c['lower_bound']+=1
        with self.assertRaises(CertificateError):check(c)
    def test_reject_invalid_word(self):
        c=exact(cerny(4));c['word']=[0];c['upper_bound']=1
        with self.assertRaises(CertificateError):check(c)
    def test_reject_bad_transition(self):
        c=exact(cerny(4));c['automaton']['transitions'][0][0]=999
        with self.assertRaises(CertificateError):check(c)
    def test_reject_truncated_potential(self):
        c=exact(cerny(4));c['potential'].pop()
        with self.assertRaises(CertificateError):check(c)
    def test_nonsynchronizing_permutations(self):
        a={'n':3,'letters':['a','b'],'transitions':[[1,2,0],[2,0,1]]}
        c=exact(a)
        self.assertEqual(c['kind'],'nonsynchronizing')
        self.assertTrue(check(c)['verified'])
    def test_reject_false_nonsynchronizing_invariant(self):
        c={'schema':'orion.sync-certificate.v1','kind':'nonsynchronizing',
           'automaton':cerny(3),'closed_masks':[7]}
        with self.assertRaises(CertificateError):check(c)
    def test_one_state_empty_word(self):
        a={'n':1,'letters':['a'],'transitions':[[0]]}
        c=exact(a)
        self.assertEqual(c['word'],[]);self.assertEqual(c['lower_bound'],0)
        self.assertTrue(check(c)['verified'])
    def test_exact_requires_equal_bounds(self):
        c,_=abstract(cerny(4),'cardinality');c['kind']='exact'
        with self.assertRaises(CertificateError):check(c)

if __name__=='__main__':unittest.main()

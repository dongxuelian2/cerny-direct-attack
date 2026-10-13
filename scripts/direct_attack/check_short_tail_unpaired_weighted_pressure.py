"""Retained OPEN-region weighted cuts; solved physical paired forms excluded."""
from pathlib import Path
import json
import copy
from .check_short_tail_opposite_weighted_pressure import check as original_check

ROOT=Path(__file__).resolve().parents[2]
NAMES=['short_tail_unpaired_weighted_M8','short_tail_unpaired_weighted_M10','short_tail_unpaired_weighted_M12_sample2000',
    'short_tail_unpaired_weighted_M14_sample1000','short_tail_unpaired_weighted_M16_sample500',
    'short_tail_unpaired_weighted_M18_sample250','short_tail_unpaired_weighted_M20_sample100']


def check(z):
    result=original_check(z);assert not result['paired_class'];return result


def main():
    data=[json.loads((ROOT/'scripts/direct_attack/data'/ (name+'.json')).read_text()) for name in NAMES]
    out=[check(z) for z in data];rejected=[]
    for mode in range(4):
        bad=copy.deepcopy(data[0])
        if mode==0:bad['peak']-=1
        if mode==1:bad['cut']=[x for x in bad['cut'] if x[0]!=bad['subset']]
        if mode==2:bad['word'].pop()
        if mode==3:bad=json.loads((ROOT/'scripts/direct_attack/data/short_tail_opposite_weighted_M8.json').read_text())
        try:check(bad)
        except(AssertionError,ValueError,KeyError):rejected.append(mode)
        else:raise AssertionError(('accepted corruption',mode))
    # A sum of two point differences need not distinguish residue multisets.
    U={0,1,2};positive={0,3};negative={1,4}
    assert all(sum((x+s)%6 in U for x in positive)==sum((x+s)%6 in U for x in negative) for s in range(6))
    assert all(any(((q+t)%6 in U)!=(q in U) for q in range(6)) for t in range(1,6))
    print(json.dumps(dict(verified=True,controls=out,corruptions_rejected=rejected,
        constant_8_unpaired_weighted_bound='REFUTED by the retained M18 minimum9',
        point_sum_multiset_identification='REFUTED literal period6 control; two-point uniqueness does not extend to sums',
        proposal_counts='EXPLORATORY'),sort_keys=True))


if __name__=='__main__':main()

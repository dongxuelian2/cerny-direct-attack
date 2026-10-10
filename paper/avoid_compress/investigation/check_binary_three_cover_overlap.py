"""Literal induced-map check of the symbolic binary overlap exclusion."""
from itertools import permutations
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent

def main():
 B={0,1,2};x=0;patterns=[];maps=0;rejected=0
 for beta in sorted(B):
  for Fx,Fc in permutations(sorted(B-{beta})):
   if Fx==x:continue
   maps+=1
   def Fpoint(p):return Fx if p==x else Fc
   for p in sorted(B):
    f=Fpoint(p)
    assert f!=beta
    fixed_M=(p==beta);fixed_F=(p==f)
    assert not (fixed_M and fixed_F)
    if not (fixed_M or fixed_F):rejected+=1;continue
    T=f if fixed_M else beta
    TF=Fpoint(T);TM=beta
    assert len({p,T,TF})==3
    # Rank-two projection forces equality with the unique matching image.
    assert TM in (p,T)
    forced_equal='S' if TM==p else 'T'
    assert forced_equal==('S' if fixed_M else 'T')
    assert (p==x)!=(T==x)
    # For a set meeting B,C once, outside c occurs iff its B-point is not x.
    assert (p!=x)!=(T!=x)
    patterns.append(dict(beta=beta,Fx=Fx,Fc=Fc,S_B=p,T_B=T,TF_B=TF,TM_B=TM,
     fixed_first_letter='M' if fixed_M else 'F',forced_M_image_equality=forced_equal,
     S_contains_c=p!=x,T_contains_c=T!=x,contradicts_outside_injectivity=True))
 assert maps==4 and len(patterns)==6 and rejected==6
 files=['BINARY_THREE_COVER_OVERLAP.md',Path(__file__).name,
  'SECOND_ENTRANCE_FIBER.md','ENTRY_FIBER_FLAG.md','LOCAL_EQUALITY_FLAG.md']
 result=dict(status='pass',induced_maps=maps,initial_choices=12,first_line_rejected=rejected,
  contradiction_patterns=len(patterns),patterns=patterns,binary_excluded_orbit='b3_in_c2',
  unrestricted_excluded_orbits=[],source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files},
  scope='Symbolic binary conditional exclusion plus a complete literal four-map check; no new F maximum or alphabet separation.')
 (ROOT/'binary_three_cover_overlap_audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({key:value for key,value in result.items() if key not in ('patterns','source_sha256','scope')}))
if __name__=='__main__':main()

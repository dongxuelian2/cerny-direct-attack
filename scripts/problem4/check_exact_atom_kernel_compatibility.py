"""Complete indexed-partition/map comparison of the exact atom criteria."""
from pathlib import Path
from itertools import product,combinations
import json,hashlib
ROOT=Path(__file__).resolve().parent
def main():
    stats=[];partition_cases=map_cases=protected_cases=0
    for n in (2,3,4):
        maps=list(product(range(n),repeat=n));pairs=list(combinations(range(n),2));Q=set(range(n));K={0,1}
        classified=[]
        for row in maps:
            kernel={p for p in pairs if row[p[0]]==row[p[1]]}
            rank=len(set(row));assert (rank==n)==(not kernel)
            if rank==n-1:assert len(kernel)==1
            classified.append((row,rank,next(iter(kernel)) if rank==n-1 else None))
        for cells in (1,2,3,4):
            labels=list(product(range(cells),repeat=n));parts=transforms=protected=0
            for target in labels:
                buckets={source:[] for source in labels}
                for row,rank,e in classified:
                    transforms+=1
                    if rank<n-1:continue
                    source=tuple(target[row[q]] for q in range(n))
                    mask=sum(1<<q for q in {row[k] for k in K})
                    buckets[source].append((rank,e,mask))
                caps=[target.count(i) for i in range(cells)]
                for source in labels:
                    parts+=1;counts=[source.count(i) for i in range(cells)]
                    perm=counts==caps
                    kernels={e for e in pairs if source[e[0]]==source[e[1]]
                             and all(counts[i]-int(i==source[e[0]])<=caps[i] for i in range(cells))}
                    raw_perm=any(rank==n for rank,e,mask in buckets[source])
                    raw_kernels={e for rank,e,mask in buckets[source] if rank==n-1}
                    assert (perm,kernels)==(raw_perm,raw_kernels)
                    for Jmask in range(1<<n):
                        protected+=1
                        permitted=any(not Jmask>>t&1 and target[t]==source[k] for t in range(n) for k in K)
                        actual_perm=any(rank==n and mask&~Jmask for rank,e,mask in buckets[source])
                        actual_kernels={e for rank,e,mask in buckets[source] if rank==n-1 and mask&~Jmask}
                        assert actual_perm==(perm and permitted)
                        assert actual_kernels==(kernels if permitted else set())
            partition_cases+=parts;map_cases+=transforms;protected_cases+=protected
            stats.append(dict(n=n,indexed_atoms=cells,input_output_partition_pairs=parts,
                              map_output_partition_instances=transforms,protected_set_cases=protected))
    assert (partition_cases,map_cases,protected_cases)==(77598,93444,1198200)
    names=[Path(__file__).name,'PROOF.md#problem4-exact-atom-kernel-compatibility']
    report=dict(status='pass',state_range='all finite nonempty Q; kernel pair requires n>=2',
                complete_partition_pairs=partition_cases,complete_map_output_instances=map_cases,
                complete_protected_set_cases=protected_cases,stats=stats,
                source_sha256={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names},
                scope='Uniform exact letter-atom realizability criterion, validated against all indexed small partitions/maps. No automaton equality claim.')
    (ROOT/'exact_atom_kernel_compatibility_audit.json').write_bytes((json.dumps(report,indent=2)+'\n').encode())
    print(json.dumps({k:v for k,v in report.items() if k not in ('source_sha256','stats')}),flush=True)
if __name__=='__main__':main()

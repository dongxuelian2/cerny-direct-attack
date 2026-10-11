"""Adversarial first-pair metadata controls of the actual generic checker.

Native domains are reconstructed once before the controls. A sentinel
at the first literal-pool call prevents rejection through later output
overwrite guards from masquerading as metadata rejection.
Full literal and flag proofs are checked by the separate case audits.
"""
from pathlib import Path
from hashlib import sha256
import argparse,copy,json,sys
import check_few_graph_case as checker
ROOT=Path(__file__).resolve().parent
def read(n):return json.loads((ROOT/n).read_text())
def digest(p):return sha256(p.read_bytes()).hexdigest()
class MetadataPassed(Exception):pass
def sentinel(*args,**kwargs):raise MetadataPassed
def exercise(scopefile,scope,data,name,native):
    oldread,oldverify,oldpool,oldargv=checker.read,checker.verify_geometry,checker.literal_pool,sys.argv
    datafile=name+'_'+scope['output_tag']+'_inventory.json'
    try:
        checker.read=lambda n:copy.deepcopy(scope) if n==scopefile else copy.deepcopy(data) if n==datafile else oldread(n)
        checker.verify_geometry=lambda *args:native
        checker.literal_pool=sentinel
        sys.argv=['check_few_graph_case.py',name,'--scope',scopefile]
        try:checker.main()
        except MetadataPassed:return 'metadata_passed'
        except AssertionError:return 'metadata_rejected'
        raise AssertionError('Checker returned without reaching the sentinel')
    finally:
        checker.read,checker.verify_geometry,checker.literal_pool,sys.argv=oldread,oldverify,oldpool,oldargv
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--scope',required=True);args=ap.parse_args()
    scope=read(args.scope);parents=read(scope['parent_domains'])['records']
    inv=read('small_first_third_inventory.json')['records'];ns=read('three_cover_atom_kernel_inventory.json')['records']
    native={};positive=[];sources={Path(__file__).name,args.scope,scope['parent_domains'],'check_few_graph_case.py',
                                'check_b1_b2_inverse_union.py','small_first_third_inventory.json','three_cover_atom_kernel_inventory.json'}
    for name in scope['selected']:
        entry=next(e for e in scope['records'] if e['id']==name)
        parent=next(e for e in parents if e['id']==name)
        native[name]=checker.verify_geometry(parent,next(e for e in inv if e['id']==name),next(e for e in ns if e['id']==name))
        assert native[name]==entry['parent_domain']
        file=name+'_'+scope['output_tag']+'_inventory.json';data=read(file)
        auditfile=name+'_'+scope['output_tag']+'_audit.json';audit=read(auditfile);assert audit['status']=='pass'
        for obj in (data,audit):
            for f,h in obj['source_sha256'].items():assert digest(ROOT/f)==h,f;sources.add(f)
        assert exercise(args.scope,scope,data,name,native[name])=='metadata_passed'
        positive.append(dict(id=name,retained_classes=audit['global_classes'],prefixes=audit['checked_prefixes']))
        sources.update([file,auditfile])
    name=scope['selected'][0];original=read(name+'_'+scope['output_tag']+'_inventory.json')
    tests=[]
    def test(label,mutate):
        s,d=copy.deepcopy(scope),copy.deepcopy(original);entry=next(e for e in s['records'] if e['id']==name)
        mutate(s,d,entry)
        assert exercise(args.scope,s,d,name,native[name])=='metadata_rejected',label
        tests.append(label)
    test('missing graph class',lambda s,d,e:e['classes'].pop())
    test('wrong graph G',lambda s,d,e:e['classes'][0]['G'].pop())
    test('missing feasible frame',lambda s,d,e:e['classes'][0]['frames'].pop())
    test('missing labelled first pair',lambda s,d,e:e['transports'].pop())
    test('duplicated labelled first pair',lambda s,d,e:e['transports'].append(copy.deepcopy(e['transports'][0])))
    test('missing representative',lambda s,d,e:e['prefixes'].pop())
    test('duplicated representative',lambda s,d,e:e['prefixes'].append(copy.deepcopy(e['prefixes'][0])))
    test('wrong multiplicity',lambda s,d,e:e['prefixes'][0].__setitem__('multiplicity',e['prefixes'][0]['multiplicity']+1))
    test('non-bijective transport',lambda s,d,e:e['transports'][0]['permutation'].__setitem__(0,e['transports'][0]['permutation'][1]))
    def swap_protected(s,d,e):
        p=e['transports'][0]['permutation'];p[3],p[10]=p[10],p[3]
    test('unprotected A transport',swap_protected)
    test('missing saved prefix',lambda s,d,e:d['prefixes'].pop())
    test('wrong target parameter',lambda s,d,e:s.__setitem__('parameter',[13,9,2]))
    assert len(tests)==12
    out=dict(status='pass',parameter=[13,9,1],target_ac=12,positive_metadata_controls=positive,
             independently_verified_native_domains=len(positive),rejected_invalid_metadata=len(tests),rejected_records=tests,
             scope='Metadata controls only; full literal/flag checks are the case audits. No new F value.',
             source_sha256={n:digest(ROOT/n) for n in sorted(sources)})
    output=ROOT/(scope['output_tag']+'_controls_audit.json');assert not output.exists()
    output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()

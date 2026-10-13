"""Controls for empty forced sets, triple products and SC-escape mode."""
from hashlib import sha256
import json
from pathlib import Path
from supplier_escape_words import certificate
from check_supplier_escape_words import check_certificate
HERE=Path(__file__).resolve().parent
def digest(p):return sha256(p.read_bytes()).hexdigest()
def main():
    source='b2_mixed_c4_third2_supplier_image_from638_v2_probe.json';c=json.loads((HERE/source).read_text())['candidate'];rows=c['rows']
    old=json.loads((HERE/'supplier_products_audit_20261012.json').read_text())['proof'];R=[sum(1<<i for i in g) for g in c['required_groups']]
    sc=dict(kind='SC_escape',state=8,forced=[66],supplier_group=2,cases=old['cases'])
    assert check_certificate(rows,(1<<219)-1,R,c['basis'][0],11,9,8,sc)==1152
    duplicated=rows+[list(rows[66])]
    domains=[(1<<66)|(1<<219),R[2],R[5]]
    p=certificate(duplicated,(1<<220)-1,domains,c['basis'][0],11,9,8)
    assert p is not None and p['kind']=='suppliers' and p['groups']==[0,1,2] and p['forced']==[]
    assert check_certificate(duplicated,(1<<220)-1,domains,c['basis'][0],11,9,8,p)==2304
    rejected=0
    for changes in [dict(state=5),dict(state=13)]:
        d=dict(sc,**changes)
        try:check_certificate(rows,(1<<219)-1,R,c['basis'][0],11,9,8,d)
        except AssertionError:rejected+=1
        else:raise AssertionError('Accepted a corrupted connectivity premise')
    out=dict(status='pass',SC_escape_words_checked=1152,triple_words_checked=2304,empty_forced_set_admitted=True,
        duplicated_literal_labels_admitted=True,SC_premise_corruptions_rejected=rejected,no_geometry_exclusion=True,no_new_numerical_extremum=True,
        source_sha256={n:digest(HERE/n) for n in [Path(__file__).name,'supplier_escape_words.py','check_supplier_escape_words.py',
            'PROOF.md#problem4-supplier-escape-words',source,'supplier_products_audit_20261012.json']})
    dest=HERE/'supplier_product_extensions_audit_20261012.json';assert not dest.exists()
    dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}),flush=True)
if __name__=='__main__':main()

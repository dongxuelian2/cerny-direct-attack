#!/usr/bin/env python3
"""ORION SyncLab: deterministic local experiments, without third-party packages."""
from __future__ import annotations
import argparse
import csv
import json
import platform
import random
import sys
import time
from pathlib import Path
from src.engine import cerny, exact, abstract, FEATURES, write_json, SEED
from src.check_certificate import check, read_json, validate_automaton

ROOT=Path(__file__).resolve().parent

def csv_write(path,rows):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    if rows:
        with p.open('w',encoding='utf-8',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def get_a(args):
    return read_json(args.input) if args.input else cerny(args.n)

def demo(args):
    out=Path(args.out)
    rows=[]
    for n in range(2,args.max_n+1):
        a=cerny(n);t=time.perf_counter();cert=exact(a)
        check(cert);elapsed=time.perf_counter()-t
        expected=(n-1)**2
        if cert['lower_bound']!=expected:
            raise RuntimeError(f'C{n} regression failed')
        write_json(out/f'C{n}.json',cert)
        row={'case':f'C{n}','n':n,'lower_bound':cert['lower_bound'],
             'upper_bound':cert['upper_bound'],'verified':True,'seconds':round(elapsed,6)}
        rows.append(row)
        print(f"C{n}: lower={expected} upper={expected} VERIFIED")
    csv_write(out/'summary.csv',rows)
    write_json(out/'environment.json',{'python':sys.version,'platform':platform.platform(),'seed':SEED})
    print(f'Output: {out.resolve()}')

def solve(args):
    cert=exact(get_a(args));write_json(args.out,cert)
    print(json.dumps(check(cert),indent=2))
    print(f'Certificate: {Path(args.out).resolve()}')

def compare(args):
    a=get_a(args);ex=exact(a);out=Path(args.out);rows=[]
    for mode in FEATURES:
        cert,row=abstract(a,mode,ex);rows.append(row)
        write_json(out/f'{mode}.json',cert)
        print(f"{mode:14} classes={row['abstract_classes']:5} lower={row['lower_bound']:4} optimal={row['optimal_length']:4}")
    csv_write(out/'comparison.csv',rows)
    print(f'Output: {out.resolve()}')

def mutate(args):
    if not 2<=args.n<=10:
        raise ValueError('Single-transition scan is restricted to 2 <= n <= 10')
    base=cerny(args.n);out=Path(args.out);results=[]
    count=0
    for letter in range(2):
        for state in range(args.n):
            old=base['transitions'][letter][state]
            for target in range(args.n):
                if target==old:continue
                a=json.loads(json.dumps(base))
                a['name']=f'C{args.n}_letter{letter}_state{state}_to{target}'
                a['transitions'][letter][state]=target
                cert=exact(a);count+=1
                row={'case':a['name'],'changed_letter':letter,'changed_state':state,
                     'old_target':old,'new_target':target,'synchronizing':cert['kind']!='nonsynchronizing',
                     'reset_length':cert.get('upper_bound','')}
                results.append(row);write_json(out/'certificates'/f"{a['name']}.json",cert)
    csv_write(out/'mutation_scan.csv',results)
    write_json(out/'scope.json',{'n':args.n,'scanned_labelled_automata':count,
               'scope':'Exactly one transition differs from the labelled Cerny baseline. No isomorphism reduction; no universal classification claim.'})
    print(f'Scanned {count} labelled one-transition changes. All certificates checked.')
    print(f'Output: {out.resolve()}')

def verify(args):
    print(json.dumps(check(read_json(args.certificate)),indent=2))

def witness(args):
    cert=read_json(args.certificate);check(cert)
    if cert['kind']=='nonsynchronizing':
        raise ValueError('This certificate has no reset word')
    a=cert['automaton'];n,letters,rows=validate_automaton(a)
    states=list(range(n));print('start:',states)
    for i,x in enumerate(cert['word'],1):
        states=sorted({rows[x][q] for q in states})
        print(f'{i:3} {letters[x]} -> {states}')
    print('length:',len(cert['word']))

def export_lean(args):
    cert=read_json(args.certificate);check(cert)
    from src.lean_export import export
    output=export(cert,ROOT/'lean'/'CertificateCore.lean')
    p=Path(args.out);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(output,encoding='utf-8')
    print(f'Lean source generated: {p.resolve()}')
    print('STATUS: source draft; compile with the pinned Lean toolchain before making a formal-verification claim.')

def landmarks(args):
    from src.engine import landmark_experiment
    a=get_a(args);n,_,_=validate_automaton(a);out=Path(args.out);rows=[]
    for r in range(n+1):
        cert,row=landmark_experiment(a,r);rows.append(row)
        write_json(out/f'r{r}.json',cert)
        print(f"r={r:2} classes={row['abstract_classes']:5} lower={row['lower_bound']:4} optimal={row['optimal_length']:4}")
    csv_write(out/'landmarks.csv',rows)
    print(f'Output: {out.resolve()}')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    sp=p.add_subparsers(dest='command',required=True)
    d=sp.add_parser('demo');d.add_argument('--max-n',type=int,default=8);d.add_argument('--out',default='results/demo');d.set_defaults(func=demo)
    s=sp.add_parser('solve');s.add_argument('--n',type=int,default=4);s.add_argument('--input');s.add_argument('--out',default='results/certificate.json');s.set_defaults(func=solve)
    s=sp.add_parser('compare');s.add_argument('--n',type=int,default=8);s.add_argument('--input');s.add_argument('--out',default='results/compare');s.set_defaults(func=compare)
    s=sp.add_parser('mutate');s.add_argument('--n',type=int,default=6);s.add_argument('--out',default='results/mutations');s.set_defaults(func=mutate)
    s=sp.add_parser('landmarks');s.add_argument('--n',type=int,default=8);s.add_argument('--input');s.add_argument('--out',default='results/landmarks');s.set_defaults(func=landmarks)
    s=sp.add_parser('verify');s.add_argument('certificate');s.set_defaults(func=verify)
    s=sp.add_parser('witness');s.add_argument('certificate');s.set_defaults(func=witness)
    s=sp.add_parser('export-lean');s.add_argument('certificate');s.add_argument('--out',default='lean/Generated.lean');s.set_defaults(func=export_lean)
    args=p.parse_args()
    try:
        args.func(args)
    except (ValueError,OSError,KeyError,TypeError,RuntimeError) as e:
        p.exit(2,f'ERROR: {e}\n')

if __name__=='__main__':
    main()

"""Compile a research kernel on demand; no build receipts or hashes."""
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]


def compile_source(name):
    source = Path(__file__).with_name(name)
    out = ROOT / 'build/bin/direct_attack' / source.stem
    out.parent.mkdir(parents=True, exist_ok=True)
    headers = list(source.parent.glob('*.hpp')) + list(source.parent.glob('*.h'))
    if not out.exists() or any(p.stat().st_mtime > out.stat().st_mtime for p in [source, *headers, Path(__file__)]):
        compiler = shutil.which(os.environ.get('CXX', 'g++'))
        if not compiler:
            raise RuntimeError('Install a C++17 compiler or set CXX.')
        subprocess.run([compiler, '-O3', '-std=c++17', '-pthread', str(source), '-o', str(out)], check=True)
    return out

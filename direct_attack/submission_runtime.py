"""Select an installed compiler without downloading or changing elan settings."""
import os
from pathlib import Path
import shutil


def lean_compiler():
    selected = os.environ.get('ORION_LEAN')
    if selected:
        resolved = shutil.which(selected)
        if resolved:
            return Path(resolved)
        path = Path(selected)
        assert path.is_file(), 'ORION_LEAN must name an installed Lean executable'
        return path
    folder = Path.home() / '.elan/toolchains/leanprover--lean4---v4.19.0/bin'
    for name in ('lean.exe', 'lean'):
        path = folder / name
        if path.is_file():
            return path
    resolved = shutil.which('lean')
    assert resolved, 'Install Lean 4.19.0 and set ORION_LEAN or PATH'
    return Path(resolved)

"""Static source consistency only: NOT a TeX/PDF compilation check."""
from pathlib import Path
import re


def main():
    source=Path(__file__).with_name('manuscript.tex').read_text(encoding='utf-8')
    stack=[]
    for match in re.finditer(r'\\(begin|end)\{([^}]+)\}',source):
        operation,environment=match.groups()
        if operation=='begin':
            stack.append(environment)
        else:
            assert stack and stack.pop()==environment
    assert not stack
    stripped=re.sub(r'\\[{}%]', '',source)
    stripped=re.sub(r'%[^\n]*', '',stripped)
    depth=0
    for char in stripped:
        depth+=(char=='{')-(char=='}')
        assert depth>=0
    assert depth==0
    labels=re.findall(r'\\label\{([^}]+)\}',source)
    assert len(labels)==len(set(labels))
    refs=re.findall(r'\\(?:ref|eqref)\{([^}]+)\}',source)
    assert set(refs)<=set(labels)
    bibliography=set(re.findall(r'\\bibitem\{([^}]+)\}',source))
    citations={key for group in re.findall(r'\\cite\{([^}]+)\}',source) for key in group.split(',')}
    assert citations<=bibliography
    assert not re.search(r'\\(?:input|include)\{',source)
    print('Static manuscript checks: balanced environments/braces, unique labels, all refs/cites resolved; PDF COMPILATION UNVERIFIED')


if __name__=='__main__':
    main()

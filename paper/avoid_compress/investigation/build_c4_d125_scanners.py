"""Specialize two verified independent algorithms to unsplit C4/D125 atoms."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def replace(s,a,b,count=1):
    assert s.count(a)==count,(a,s.count(a),count)
    return s.replace(a,b)
def main():
    for role in ('rows','forward'):
        s=(ROOT/f'check_d15_d25_fourth_{role}.cpp').read_text()
        s=s.replace('D15/D25','C4/D125')
        s=replace(s,'(mode==15||mode==25)','mode==125')
        s=replace(s,'atoms==(mode==15?6:5)','atoms==5')
        s=replace(s,'int dm=mode==15?((1<<1)|(1<<5)):((1<<2)|(1<<5));','int dm=(1<<1)|(1<<2)|(1<<5);')
        s=replace(s,'pop(S&((1<<1)|(1<<4)))==1' if role=='rows' else 'bits(S&((1<<1)|(1<<4)))==1',
          '(S>>4&1)')
        s=replace(s,'forms.size()<=60','forms.size()<=45')
        s=s.replace('uint64_t(1)<<59','uint64_t(1)<<44')
        if role=='rows':s=replace(s,')>>59==1',')>>44==1')
        where='fixed_states=(hm>>6&1)?7:6;' if role=='rows' else 'int fixed_states=(hm>>6&1)?7:6;'
        s=replace(s,where,('require' if role=='rows' else 'must')+'(hm==64||hm==66||hm==70);'+('fixed_states=7;' if role=='rows' else 'int fixed_states=7;'))
        Path(ROOT/f'check_c4_d125_fourth_{role}.cpp').write_text(s)
    print('Generated two specialized C4/D125 scanners; older audited sources unchanged.')
if __name__=='__main__':main()

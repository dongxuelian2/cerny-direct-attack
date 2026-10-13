"""Generalize audited binary row scans to all remaining D15/D25 fields."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def replace(s,a,b,count=1):
    assert s.count(a)==count,(a,s.count(a),count)
    return s.replace(a,b)

def main():
    s=(ROOT/'check_d12_d24_fourth_rows.cpp').read_text()
    s=replace(s,'// C++17 complete D12/D24 fourth rows with exact cached 5040-element orbits.',
        '// C++17 complete D15/D25 fourth rows; exact 720/5040-element orbit caches.')
    s=replace(s,'(mode==12||mode==24)','(mode==15||mode==25)')
    s=replace(s,'atoms==6','atoms==(mode==15?6:5)')
    s=replace(s,'std::map<Row,std::pair<Row,Row>> norm_cache;',
        'int fixed_states=7;std::map<Row,std::pair<Row,Row>> norm_cache;')
    a='''static const std::vector<Row> group=[](){
        Row g;for(int q=0;q<13;q++)g[q]=q;std::vector<Row> all;
        do{all.push_back(g);}while(std::next_permutation(g.begin()+6,g.end()));
        require(all.size()==5040);return all;
    }();'''
    b='''static std::map<int,std::vector<Row>> groups;
    auto& group=groups[fixed_states];
    if(group.empty()){
        Row g;for(int q=0;q<13;q++)g[q]=q;
        do{group.push_back(g);}while(std::next_permutation(g.begin()+fixed_states,g.end()));
    }
    require(group.size()==size_t(fixed_states==7?720:5040));'''
    s=replace(s,a,b)
    s=replace(s,'require(hm==(1<<5)||hm==((1<<1)|(1<<5))||hm==((1<<2)|(1<<5)));int dm=mode==12?((1<<1)|(1<<2)):((1<<2)|(1<<4));',
        'fixed_states=(hm>>6&1)?7:6;int dm=mode==15?((1<<1)|(1<<5)):((1<<2)|(1<<5));')
    s=replace(s,'require(forms.size()==size_t(hm==(1<<5)?56:42));require((uint64_t(1)<<55)>>55==1);',
        'require(!forms.empty()&&forms.size()<=60);require((uint64_t(1)<<59)>>59==1);')
    (ROOT/'check_d15_d25_fourth_rows.cpp').write_text(s,encoding='utf-8')

    s=(ROOT/'check_d12_d24_fourth_forward.cpp').read_text()
    s=replace(s,'// Independent D12/D24 fourth domains, pointwise transports and forward coupled check.',
        '// Independent D15/D25 fourth domains, pointwise transports and forward coupled check.')
    s=replace(s,'(mode==12||mode==24)','(mode==15||mode==25)')
    s=replace(s,'atoms==6','atoms==(mode==15?6:5)')
    s=replace(s,'must(hm==(1<<5)||hm==((1<<1)|(1<<5))||hm==((1<<2)|(1<<5)));int dm=mode==12?((1<<1)|(1<<2)):((1<<2)|(1<<4));',
        'int fixed_states=(hm>>6&1)?7:6;int dm=mode==15?((1<<1)|(1<<5)):((1<<2)|(1<<5));')
    s=replace(s,'must(forms.size()==size_t(hm==(1<<5)?56:42));must(__builtin_popcountll((uint64_t(1)<<55)|1)==2);',
        'must(!forms.empty()&&forms.size()<=60);must(__builtin_popcountll((uint64_t(1)<<59)|1)==2);')
    s=replace(s,'if(q<6)must(g[q]==q);','if(q<fixed_states)must(g[q]==q);')
    (ROOT/'check_d15_d25_fourth_forward.cpp').write_text(s,encoding='utf-8')
    print('Generated fresh complete D15/D25 scanners; older audited files unchanged.')
if __name__=='__main__':main()

"""Generalize the immutable D125 algorithms to six D12/D24 domains."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def replace(s,a,b,count=1):
    assert s.count(a)==count,(a,s.count(a),count)
    return s.replace(a,b)

def main():
    s=(ROOT/'check_d125_fourth_rows.cpp').read_text()
    s=replace(s,'// C++17 complete D125/E6,E26 rows and ordinary-conjugacy binary pairs.',
        '// C++17 complete D12/D24 fourth rows with exact cached 5040-element orbits.')
    s=replace(s,'if(argc!=4)return 2;','if(argc!=5)return 2;')
    s=replace(s,'transport(argv[3],std::ios::binary);require(bool(input)&&bool(dump)&&bool(transport));',
        'transport(argv[3],std::ios::binary),kept(argv[4],std::ios::binary);require(bool(input)&&bool(dump)&&bool(transport)&&bool(kept));')
    s=replace(s,'(mode==6||mode==26)','(mode==12||mode==24)')
    s=replace(s,'forms.clear();form_flag.fill(false);','norm_cache.clear();forms.clear();form_flag.fill(false);')
    s=replace(s,'require(hm==(mode==6?(1<<6):((1<<2)|(1<<6))));',
        'require(hm==(1<<5)||hm==((1<<1)|(1<<5))||hm==((1<<2)|(1<<5)));int dm=mode==12?((1<<1)|(1<<2)):((1<<2)|(1<<4));')
    s=replace(s,'pop(S&((1<<1)|(1<<2)|(1<<5)))==1','pop(S&dm)==1')
    s=replace(s,'require(forms.size()==size_t(mode==6?36:27)); require((uint64_t(1)<<35)>>35==1);',
        'require(forms.size()==size_t(hm==(1<<5)?56:42));require((uint64_t(1)<<55)>>55==1);')
    start=s.index('std::pair<Row,Row> normalize(');end=s.index('uint64_t transport_mask(',start)
    s=s[:start]+r'''
std::map<Row,std::pair<Row,Row>> norm_cache;
std::pair<Row,Row> normalize(const Row& f){
    auto found=norm_cache.find(f);if(found!=norm_cache.end())return found->second;
    static const std::vector<Row> group=[](){
        Row g;for(int q=0;q<13;q++)g[q]=q;std::vector<Row> all;
        do{all.push_back(g);}while(std::next_permutation(g.begin()+6,g.end()));
        require(all.size()==5040);return all;
    }();
    Row best=f,g0=group.front();
    for(const Row& g:group){Row can;for(int q=0;q<13;q++)can[g[q]]=g[f[q]];
        if(can<best){best=can;g0=g;}}
    for(const Row& g:group){Row can,k;
        for(int q=0;q<13;q++){can[g[q]]=g[f[q]];k[g[q]]=g0[q];}
        norm_cache.emplace(can,std::make_pair(best,k));}
    auto result=norm_cache.find(f);require(result!=norm_cache.end());return result->second;
}
''' +s[end:]
    s=replace(s,'models[f].push_back(model(row,mask));hist["kept"]++;', '''models[f].push_back(model(row,mask));hist["kept"]++;
                kept<<mode<<" "<<hm<<" "<<f<<" "<<mask;for(int t:row)kept<<" "<<t;kept<<"\\n";''')
    s=replace(s,'require(bool(dump)&&bool(transport));','require(bool(dump)&&bool(transport)&&bool(kept));')
    (ROOT/'check_d12_d24_fourth_rows.cpp').write_text(s,encoding='utf-8')

    s=(ROOT/'check_d125_fourth_forward.cpp').read_text()
    s=replace(s,'// Independent D125 fourth domain, pointwise transports and forward coupled check.',
        '// Independent D12/D24 fourth domains, pointwise transports and forward coupled check.')
    s=replace(s,'(mode==6||mode==26)','(mode==12||mode==24)')
    s=replace(s,'must(hm==(mode==6?(1<<6):((1<<2)|(1<<6))));',
        'must(hm==(1<<5)||hm==((1<<1)|(1<<5))||hm==((1<<2)|(1<<5)));int dm=mode==12?((1<<1)|(1<<2)):((1<<2)|(1<<4));')
    s=replace(s,'bits(S&((1<<1)|(1<<2)|(1<<5)))==1','bits(S&dm)==1')
    s=replace(s,'must(forms.size()==size_t(mode==6?36:27));must(__builtin_popcountll((uint64_t(1)<<35)|1)==2);',
        'must(forms.size()==size_t(hm==(1<<5)?56:42));must(__builtin_popcountll((uint64_t(1)<<55)|1)==2);')
    s=replace(s,'if(q<7)must(g[q]==q);','if(q<6)must(g[q]==q);')
    extra=r'''
uint64_t forward_safe_initials(uint64_t allowed,const Letter& a,const Letter& b){
    uint64_t safe=0;
    for(size_t i=0;i<forms.size();i++)if(allowed>>i&1){
        std::vector<int> layer={forms[i]};bool good=true;
        for(int depth=1;depth<=11&&good;depth++){
            std::array<bool,8192> marked{};std::vector<int> next;
            for(int S:layer)for(const Row* r:{&a.r,&b.r}){
                int T=map_set(S,*r);
                if(bits(T)!=9||!(T>>3&1)||(depth<=7&&!std::binary_search(forms.begin(),forms.end(),T))){good=false;break;}
                if(!marked[T]){marked[T]=true;next.push_back(T);}}
            layer=next;
        }
        if(good)safe|=uint64_t(1)<<i;
    }
    return safe;
}
uint64_t forward_reached_initials(const Letter& a,const Letter& b){
    std::vector<int> todo={ALL};std::array<bool,8192> seen{};seen[ALL]=true;uint64_t result=0;
    for(size_t i=0;i<todo.size();i++){
        int S=todo[i];auto pos=std::lower_bound(forms.begin(),forms.end(),S);
        if(pos!=forms.end()&&*pos==S)result|=uint64_t(1)<<(pos-forms.begin());
        for(const Row* r:{&a.r,&b.r}){int T=map_set(S,*r);if(!seen[T]){seen[T]=true;todo.push_back(T);}}
    }
    return result;
}
'''
    s=replace(s,'void print_hist(',extra+'\nvoid print_hist(')
    s=replace(s,'hist["surviving_necessary_pair"]++;', '''uint64_t safe=forward_safe_initials(l.initial&r.initial,l,r);
            if(!safe){hist["no_safe_initial_image"]++;continue;}
            if(!(safe&forward_reached_initials(l,r))){hist["not_reachable_initial_image"]++;continue;}
            hist["surviving_reachable_pair"]++;''')
    (ROOT/'check_d12_d24_fourth_forward.cpp').write_text(s,encoding='utf-8')
    print('Generated fresh D12/D24 algorithms; frozen D125 sources unchanged.')

if __name__=='__main__':main()

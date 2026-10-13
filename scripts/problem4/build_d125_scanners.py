"""Generate fresh D125 scanners from immutable, independently designed algorithms."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def change(s,a,b,count=1):
    assert s.count(a)==count,(a,s.count(a),count)
    return s.replace(a,b)

def main():
    s=(ROOT/'check_e26_f7_seventh_rows.cpp').read_text()
    s=change(s,'// C++17 complete conditional E26/F7 seventh survivors rows and binary row pairs.',
        '// C++17 complete D125/E6,E26 rows and ordinary-conjugacy binary pairs.')
    s=change(s,'Row row;int initial_mask=0,image_mask=0;','Row row;uint64_t initial_mask=0;int image_mask=0;')
    s=change(s,'int initial_mask(const Row& row)','uint64_t initial_mask(const Row& row)')
    s=change(s,'int mask=0;','uint64_t mask=0;',2)
    s=change(s,'mask|=1<<i;','mask|=uint64_t(1)<<i;')
    s=change(s,'mask|=1<<j;','mask|=uint64_t(1)<<j;')
    s=change(s,'Model model(const Row& row,int mask)','Model model(const Row& row,uint64_t mask)')
    s=change(s,'int reachable_forms(','uint64_t reachable_forms(')
    s=change(s,'depth<=4&&!form_flag[state]','depth<=7&&!form_flag[state]')
    s=change(s,'d+1<=4&&!form_flag[out]','d+1<=7&&!form_flag[out]')
    s=change(s,'if(argc!=3)return 2;','if(argc!=4)return 2;')
    s=change(s,'std::ifstream input(argv[1]);std::ofstream dump(argv[2],std::ios::binary);require(bool(input)&&bool(dump));',
        'std::ifstream input(argv[1]);std::ofstream dump(argv[2],std::ios::binary),transport(argv[3],std::ios::binary);require(bool(input)&&bool(dump)&&bool(transport));')
    s=change(s,'(mode==8||mode==18||mode==28)','(mode==6||mode==26)')
    s=change(s,'atoms==(mode==8?8:9)','atoms==6')
    a='''forms.clear();form_flag.fill(false);int gm=(1<<8)|(mode==8?0:(1<<(mode==18?1:2)));
        protected_mask=FULL;
        for(int S=0;S<=FULL;S++)if(pop(S)==9&&(S>>3&1)&&((S&((1<<0)|(1<<5)))==((1<<0)|(1<<5)))
            &&pop(S&((1<<1)|(1<<4)))==1&&pop(S&((1<<2)|(1<<6)))==1&&(S>>7&1)&&pop(S&gm)==1&&pop(S&hm)==1){'''
    b='''forms.clear();form_flag.fill(false);
        protected_mask=FULL;
        require(hm==(mode==6?(1<<6):((1<<2)|(1<<6))));
        for(int S=0;S<=FULL;S++)if(pop(S)==9&&(S>>3&1)&&(S>>0&1)
            &&pop(S&((1<<1)|(1<<4)))==1&&pop(S&((1<<1)|(1<<2)|(1<<5)))==1&&pop(S&hm)==1){'''
    s=change(s,a,b)
    s=change(s,'require(!forms.empty()&&forms.size()<=20);',
        'require(forms.size()==size_t(mode==6?36:27)); require((uint64_t(1)<<35)>>35==1);')
    s=change(s,'std::vector<std::vector<Model>> models(field_count);',
        'std::vector<std::vector<Model>> models(field_count),reduced(field_count);')
    s=change(s,'int mask=initial_mask(row);','uint64_t mask=initial_mask(row);')
    s=change(s,'models[f].push_back(model(row,mask));hist["kept"]++;', '''models[f].push_back(model(row,mask));hist["kept"]++;
                auto rep=normalize(row);const Row& can=rep.first;const Row& g=rep.second;
                uint64_t cm=initial_mask(can);require(single_cut(can).empty()&&cm&&transport_mask(mask,g)==cm);
                require(std::binary_search(raw.begin(),raw.end(),can));
                transport<<mode<<" "<<hm<<" "<<f<<" "<<mask<<" "<<cm;
                for(int t:row)transport<<" "<<t;for(int t:g)transport<<" "<<t;for(int t:can)transport<<" "<<t;transport<<"\\n";
                reduced[f].push_back(model(can,cm));''')
    s=change(s,'raw_total+=raw.size();kept_total+=models[f].size();individual_hist.push_back(hist);', '''std::sort(reduced[f].begin(),reduced[f].end(),[](const Model& a,const Model& b){return a.row<b.row;});
            reduced[f].erase(std::unique(reduced[f].begin(),reduced[f].end(),[](const Model& a,const Model& b){return a.row==b.row;}),reduced[f].end());
            raw_total+=raw.size();kept_total+=models[f].size();individual_hist.push_back(hist);''')
    s=change(s,'uint64_t raw_pairs=0,kept_pairs=0,checked=0,candidate_images=0;',
        'uint64_t raw_pairs=0,kept_pairs=0,expected_reduced=0,checked=0,candidate_images=0;')
    s=change(s,'kept_pairs+=uint64_t(models[a].size())*models[b].size();',
        'kept_pairs+=uint64_t(models[a].size())*models[b].size();expected_reduced+=uint64_t(reduced[a].size())*models[b].size();')
    s=change(s,'for(const Model& l:models[a])for(const Model& x:models[b])',
        'for(const Model& l:reduced[a])for(const Model& x:models[b])')
    s=change(s,'checked++;int initial=l.initial_mask&x.initial_mask;','checked++;uint64_t initial=l.initial_mask&x.initial_mask;')
    s=change(s,'int safe=0;','uint64_t safe=0;')
    s=change(s,'safe|=1<<i;','safe|=uint64_t(1)<<i;')
    s=change(s,'int reached=reachable_forms(l,x)&safe;','uint64_t reached=reachable_forms(l,x)&safe;')
    s=change(s,'candidate_images+=pop(reached);','candidate_images+=__builtin_popcountll(reached);')
    s=change(s,'int i=__builtin_ctz(unsigned(reached));','int i=__builtin_ctzll(reached);')
    s=change(s,'require(checked==kept_pairs);','require(checked==expected_reduced);')
    s=change(s,'<<",\\\"kept_rows\\\":"<<models[i].size()<<",\\\"counts\\\":";',
        '<<",\\\"kept_rows\\\":"<<models[i].size()<<",\\\"representatives\\\":"<<reduced[i].size()<<",\\\"counts\\\":";')
    s=change(s,'require(input.eof());require(bool(dump));','require(input.eof());require(bool(dump)&&bool(transport));')
    functions=r'''
std::pair<Row,Row> normalize(const Row& f){
    static const std::vector<Row> group=[](){
        Row g;for(int q=0;q<13;q++)g[q]=q;std::vector<Row> all;
        do{all.push_back(g);}while(std::next_permutation(g.begin()+7,g.end()));
        require(all.size()==720);return all;
    }();
    Row best=f,chosen=group.front();
    for(const Row& g:group){Row can;for(int q=0;q<13;q++)can[g[q]]=g[f[q]];
        if(can<best){best=can;chosen=g;}}
    return {best,chosen};
}
uint64_t transport_mask(uint64_t mask,const Row& g){
    uint64_t out=0;for(size_t i=0;i<forms.size();i++)if(mask>>i&1){
        int transported=image(forms[i],g);auto it=std::lower_bound(forms.begin(),forms.end(),transported);
        require(it!=forms.end()&&*it==transported);out|=uint64_t(1)<<(it-forms.begin());}
    return out;
}
'''
    s=change(s,'struct Candidate{',functions+'\nstruct Candidate{')
    (ROOT/'check_d125_fourth_rows.cpp').write_text(s,encoding='utf-8')

    s=(ROOT/'check_e26_f7_seventh_forward.cpp').read_text()
    s=change(s,'// Independent forward verification of the complete E26/F7 seventh row domains.',
        '// Independent D125 fourth domain, pointwise transports and forward coupled check.')
    s=change(s,'#include <array>','#include <array>\n#include <set>\n#include <cstdint>')
    s=change(s,'int pure_safe_mask(const Row& r)','uint64_t pure_safe_mask(const Row& r)')
    s=change(s,'int mask=0;','uint64_t mask=0;')
    s=change(s,'mask|=1<<i;','mask|=uint64_t(1)<<i;')
    s=change(s,'length<=4&&!std::binary_search','length<=7&&!std::binary_search')
    s=change(s,'std::array<int,78> next;int initial;','std::array<int,78> next;uint64_t initial;')
    s=change(s,'Letter prepare(Row r,int initial)','Letter prepare(Row r,uint64_t initial)')
    s=change(s,'if(argc!=4)return 2;','if(argc!=5)return 2;')
    s=change(s,'std::ifstream fields(argv[1]),raw(argv[2]);std::ofstream kept(argv[3],std::ios::binary);',
        'std::ifstream fields(argv[1]),raw(argv[2]),transport(argv[3]);std::ofstream kept(argv[4],std::ios::binary);')
    s=change(s,'must(bool(fields)&&bool(raw)&&bool(kept));',
        'must(bool(fields)&&bool(raw)&&bool(transport)&&bool(kept));')
    s=change(s,'(mode==8||mode==18||mode==28)','(mode==6||mode==26)')
    s=change(s,'atoms==(mode==8?8:9)','atoms==6')
    a='''forms.clear();protected_mask=ALL;int gm=(1<<8)|(mode==8?0:(1<<(mode==18?1:2)));
        for(int S=0;S<=ALL;S++)if(bits(S)==9&&(S>>3&1)&&(S>>0&1)&&(S>>5&1)
            &&bits(S&((1<<1)|(1<<4)))==1&&bits(S&((1<<2)|(1<<6)))==1&&(S>>7&1)&&bits(S&gm)==1&&bits(S&hm)==1){'''
    b='''forms.clear();protected_mask=ALL;
        must(hm==(mode==6?(1<<6):((1<<2)|(1<<6))));
        for(int S=0;S<=ALL;S++)if(bits(S)==9&&(S>>3&1)&&(S>>0&1)
            &&bits(S&((1<<1)|(1<<4)))==1&&bits(S&((1<<1)|(1<<2)|(1<<5)))==1&&bits(S&hm)==1){'''
    s=change(s,a,b)
    s=change(s,'must(!forms.empty()&&forms.size()<=20);',
        'must(forms.size()==size_t(mode==6?36:27));must(__builtin_popcountll((uint64_t(1)<<35)|1)==2);')
    s=change(s,'std::vector<std::vector<Letter>> models(rows);',
        'std::vector<std::vector<Letter>> models(rows),reduced(rows); std::vector<std::set<Row>> representatives(rows);')
    s=change(s,'int initial=pure_safe_mask(raw_row);','uint64_t initial=pure_safe_mask(raw_row);')
    s=change(s,'individual[raw_field]["kept"]++;models[raw_field].push_back(prepare(raw_row,initial));', '''individual[raw_field]["kept"]++;models[raw_field].push_back(prepare(raw_row,initial));
                    int tm,th,tf;uint64_t om,cm;Row original,g,can;
                    must(bool(transport>>tm>>th>>tf>>om>>cm));
                    for(int& q:original)must(bool(transport>>q));for(int& q:g)must(bool(transport>>q));for(int& q:can)must(bool(transport>>q));
                    must(tm==mode&&th==hm&&tf==raw_field&&om==initial&&original==raw_row);
                    int gm=0;for(int q=0;q<13;q++){must(g[q]>=0&&g[q]<13&&!(gm>>g[q]&1));gm|=1<<g[q];if(q<7)must(g[q]==q);}
                    must(gm==ALL);for(int q=0;q<13;q++)must(can[g[q]]==g[original[q]]);
                    for(int q=0;q<13;q++)must(std::find(out[target_field[tf][q]].begin(),out[target_field[tf][q]].end(),can[q])!=out[target_field[tf][q]].end());
                    must(pure_pair_cut(can).empty()&&pure_safe_mask(can)==cm);
                    uint64_t transported=0;for(size_t j=0;j<forms.size();j++)if(om>>j&1){
                        int T=map_set(forms[j],g);auto it=std::lower_bound(forms.begin(),forms.end(),T);must(it!=forms.end()&&*it==T);
                        transported|=uint64_t(1)<<(it-forms.begin());}
                    must(cm==transported);representatives[tf].insert(can);''')
    s=change(s,'uint64_t checked=0;std::map<std::string,uint64_t> hist;', '''for(int f=0;f<rows;f++)for(const Row& can:representatives[f]){
            must(std::any_of(models[f].begin(),models[f].end(),[&](const Letter& l){return l.r==can;}));
            reduced[f].push_back(prepare(can,pure_safe_mask(can)));}
        uint64_t checked=0;std::map<std::string,uint64_t> hist;''')
    s=change(s,'for(const Letter& l:models[a])for(const Letter& r:models[b])',
        'for(const Letter& l:reduced[a])for(const Letter& r:models[b])')
    s=change(s,'uint64_t(models[a].size())*models[b].size();must(checked==expected);',
        'uint64_t(reduced[a].size())*models[b].size();must(checked==expected);')
    s=change(s,'<<",\\\"kept_rows\\\":"<<models[f].size()<<",\\\"counts\\\":";',
        '<<",\\\"kept_rows\\\":"<<models[f].size()<<",\\\"representatives\\\":"<<reduced[f].size()<<",\\\"counts\\\":";')
    s=change(s,'must(fields.eof()&&!available&&raw.eof()&&bool(kept));',
        'int extra;must(!(transport>>extra)&&transport.eof());must(fields.eof()&&!available&&raw.eof()&&bool(kept));')
    (ROOT/'check_d125_fourth_forward.cpp').write_text(s,encoding='utf-8')
    print('Generated two fresh scanners; no accepted source edited.')

if __name__=='__main__':main()

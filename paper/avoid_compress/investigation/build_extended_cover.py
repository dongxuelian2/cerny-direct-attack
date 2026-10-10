"""Extend the two audited covers without modifying the released n=11 sources.

Adds the proved short-pair cardinality prune and sufficient widths through
n=16. Generation is not a mathematical proof; completed runs and the
independent comparison are still required.
"""
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def main():
    first=(ROOT/"compression_decision.cpp").read_text()
    first=first.replace("[12]","[16]").replace(",12>",",16>")
    first=first.replace("[66]","[120]").replace("n>11","n>16")
    old="d[i]=depth;todo[tail++]=i;"
    assert old in first
    first=first.replace(old,old+"if(target==(m+2)*(m+1)/2 && depth<=m && tail>depth)return false;")
    (ROOT/"compression_decision_extended.cpp").write_text(first)

    source=(ROOT/"compression_decision_independent.cpp").read_text()
    source=source.replace("using V=std::vector<int>;using U=std::uint64_t;",r"""
using V=std::vector<int>;using W=std::uint64_t;
struct U {
 W lo=0,hi=0;
 explicit operator bool()const{return lo||hi;}
 int first()const{return lo?__builtin_ctzll(lo):64+__builtin_ctzll(hi);}
 void drop_first(){if(lo)lo&=lo-1;else hi&=hi-1;}
 int count()const{return __builtin_popcountll(lo)+__builtin_popcountll(hi);}
 U& operator|=(U x){lo|=x.lo;hi|=x.hi;return *this;}
 U& operator&=(U x){lo&=x.lo;hi&=x.hi;return *this;}
};
U bit(int i){U x;if(i<64)x.lo=W(1)<<i;else x.hi=W(1)<<(i-64);return x;}
U operator|(U x,U y){x|=y;return x;}
U operator&(U x,U y){x&=y;return x;}
U operator~(U x){x.lo=~x.lo;x.hi=~x.hi;return x;}
""")
    source=source.replace("[12]","[16]").replace(",66>",",120>")
    source=source.replace("std::array<std::array<U,3>,120> covers{};std::array<U,3> all_covers{};",
                          "std::array<std::array<W,9>,120> covers{};std::array<W,9> all_covers{};int cover_words=0;")
    source=source.replace("U(1)<<bit","W(1)<<bit")
    source=source.replace("++hole_number;}","++hole_number;}cover_words=(hole_number+63)/64;")
    source=source.replace("U(1)<<kernel_index","bit(kernel_index)")
    source=source.replace("U(1)<<preimage","bit(preimage)")
    source=source.replace("U(1)<<ix[source][q]","bit(ix[source][q])")
    source=source.replace("U(1)<<i","bit(i)")
    source=source.replace("U next=0","U next{}").replace("reverse_a.fill(0)","reverse_a.fill(U{})").replace("reverse_b.fill(0)","reverse_b.fill(U{})")
    source=source.replace("__builtin_ctzll(inspect)","inspect.first()").replace("inspect&=inspect-1","inspect.drop_first()")
    source=source.replace("__builtin_ctzll(front)","front.first()").replace("front&=front-1","front.drop_first()")
    source=source.replace("__builtin_popcountll(known)","known.count()")
    source=source.replace("w<3","w<cover_words")
    source=source.replace("if(!(available[0]|available[1]|available[2]))return false;",
                          "bool remains=false;for(int w=0;w<cover_words;++w)remains|=available[w]!=0;if(!remains)return false;")
    source=source.replace("for(int d=1;d<target;++d){",
                          "for(int d=1;d<target;++d){if(target==(budget+2)*(budget+1)/2 && d<=budget && known.count()>d)return false;")
    source=source.replace("n>11","n>16")
    assert "U(1)" not in source and "[12]" not in source and "[66]" not in source
    (ROOT/"compression_decision_extended_independent.cpp").write_text(source)
    print("wrote two widened short-cardinality covers; old release sources untouched")

if __name__=="__main__":main()

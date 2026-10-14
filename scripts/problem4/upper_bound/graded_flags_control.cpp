// Independent early versus graded flag enumeration control.
#define main flags_program_main
#include "slack_one_initial_flags.cpp"
#undef main
int main() {
 std::cout<<std::unitbuf;
 std::vector<unsigned> rows;
 for(unsigned m=0;m<8192;++m) if(__builtin_popcount(m)==9) rows.push_back(m);
 for(int split:{2,3}) {
   auto early=examine(cores[19],rows,false,true,true,true,true,3,split);
   auto generic=examine_late(cores[19],rows,false,3,split);
   std::cout<<"COMPARE core="<<cores[19].id<<" split="<<split
            <<" early_flags="<<early.pair_one<<" generic_flags="<<generic.pair_one
            <<" early_vectors="<<early.vectors<<" generic_vectors="<<generic.vectors
            <<" early_actions="<<early.actions<<" generic_actions="<<generic.actions<<'\n';
   assert(early.pair_one==generic.pair_one&&early.vectors==generic.vectors);
 }
 std::cout<<"PASS independent early and graded flag enumerations\n";
}

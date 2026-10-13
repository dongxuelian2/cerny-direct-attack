"""Research-only inverse enumeration with a proved partial reverse trap cut.

Preserves the original proof sources and the already running zero-cut covers.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
bitsets = r'''
 bool reverse_open(){
  unsigned seen=1;int queue[16],head=0,tail=1;queue[0]=0;
  while(head<tail){int q=queue[head++];
   // An unassigned incoming b-fiber can still bring new states into this set.
   if(!fiber_done[q])return true;
   for(int p=0;p<n;++p)if(shape->a[p]==q&&!(seen&(1u<<p))){seen|=1u<<p;queue[tail++]=p;}
   for(int p:fibers[q])if(!(seen&(1u<<p))){seen|=1u<<p;queue[tail++]=p;}
  }
  return seen==(1u<<n)-1;
 }
'''
numeric = r'''
 bool reverse_open(){
  bool seen[16]={};seen[0]=true;bool changed=true;
  while(changed){changed=false;
   for(int q=0;q<n;++q)if(seen[q]){
    if(!fiber_done[q])return true;
    for(int p=0;p<n;++p)if(!seen[p]&&(shape->a[p]==q||letter[p]==q)){seen[p]=true;changed=true;}
   }
  }
  for(int q=0;q<n;++q)if(!seen[q])return false;
  return true;
 }
'''
for suffix, method in (("",bitsets),("_fibers",numeric)):
    source=(ROOT/f"compression_decision_inverse_zero{suffix}.cpp").read_text(encoding="utf-8")
    needle=" int priority(unsigned position){"
    assert source.count(needle)==1
    source=source.replace(needle,method+needle)
    needle="if(prune_enabled&&position>=1&&!possible())++discarded;else traverse(position+1,nextused);"
    assert source.count(needle)==1
    source=source.replace(needle,"if(prune_enabled&&!reverse_open())++discarded;\n  else "+needle)
    source=source.replace("Inverse successor discovery, adaptive early-pair assignment and explicit hole masks.",
                          "Inverse discovery with a partial reverse-trap cut and explicit hole masks.")
    source=source.replace("Inverse discovery with zero-state connectivity cut, inverse-fiber pair BFS and recursive hole covers.",
                          "Inverse discovery with a partial reverse-trap cut, numeric pair BFS and recursive covers.")
    (ROOT/f"compression_decision_inverse_trap{suffix}.cpp").write_text(source,encoding="utf-8")
print("wrote two research variants with a partial reverse-trap cut")

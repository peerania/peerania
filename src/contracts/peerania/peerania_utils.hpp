#include <eosiolib/eosio.hpp>
#include <eosiolib/types.hpp> 
#include <iterator>  


namespace std{
template<class Iter, typename Functor>
Iter binary_find(Iter begin, Iter end, int id, Functor element_id)
{
  Iter it;
  //iterator_traits<Iter>::difference_type count, step;
  auto count = distance(begin,end);
  while (count>0)
  {
    it = begin;
    auto step=count/2; 
    advance (it,step);
    if (element_id(*it)<id) {
      begin=++it;
      count-=step+1;
    }
    else count=step;
  }
  if(begin != end && element_id(*begin) == id)
    return begin;
  return end;
}

template<class Iter, typename Functor>
Iter linear_find(Iter begin, Iter end, int key, Functor element_key){
  while(begin != end){
    if(element_key(*begin) == key)
      return begin;
    begin++;
  }
  return end;
}
}

namespace eosio{
inline time current_time_in_sec(){
    return current_time() / 1000000;
}
}
#include <pythonic/include/__builtin__/print.hpp>
#include <pythonic/include/__builtin__/str.hpp>
#include <pythonic/__builtin__/print.hpp>
#include <pythonic/__builtin__/str.hpp>
namespace __pythran_tutorial_module
{
  ;
  struct main
  {
    typedef void callable;
    ;
    struct type
    {
      typedef typename pythonic::assignable<long>::type __type0;
      typedef typename pythonic::assignable<typename pythonic::assignable<long>::type>::type __type1;
      typedef typename pythonic::returnable<typename __combined<__type0,__type1>::type>::type result_type;
    }  ;
    typename type::result_type operator()() const;
    ;
  }  ;
  typename main::type::result_type main::operator()() const
  {
    typedef typename pythonic::assignable<long>::type __type0;
    typedef typename pythonic::assignable<typename pythonic::assignable<long>::type>::type __type2;
    typedef typename pythonic::assignable<typename __combined<__type0,__type2>::type>::type __type3;
    pythonic::__builtin__::print("hello world");
    typename pythonic::assignable<typename __combined<__type0,__type2>::type>::type a = 3L;
    typename pythonic::assignable<typename __combined<__type0,__type3>::type>::type b = 4L;
    if (a < b)
    {
      a = b;
    }
    else
    {
      b = a;
    }
    return a;
  }
}
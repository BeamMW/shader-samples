////////////////////////
#include "Shaders/common.h"

#include "test_contract.h"
#include <vector>
#include <array>
#include <numeric>
#include <iterator>

BEAM_EXPORT void Ctor(void*)
{
    //std::array<uint32_t, 100> v;
    std::vector<uint32_t> v(100);
    std::iota(v.begin(), v.end(), 90);
    std::vector<uint32_t> v2;
    v2.reserve(200);
    std::copy(v.begin(), v.end(), std::back_inserter(v2));
}

BEAM_EXPORT void Dtor(void*)
{
 
}

BEAM_EXPORT void Method_2(const void*)
{
    abort();
    //std::terminate();
}

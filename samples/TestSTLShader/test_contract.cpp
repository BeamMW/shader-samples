////////////////////////
#include "Shaders/common.h"

#include "test_contract.h"
#include <vector>
#include <string>
#include <map>
#include <numeric>


BEAM_EXPORT void Ctor(void*)
{
    std::vector<uint32_t> v(100);
    std::iota(v.begin(), v.end(), 90);

    std::map<uint32_t, std::string> m;

    for (const auto& i : v)
    {
        m.emplace(i, std::to_string(i));
    }

    for (auto& p : m)
    {
        p.second = "Item: " + p.second;
    }
}

BEAM_EXPORT void Dtor(void*)
{
 
}

BEAM_EXPORT void Method_2(const void*)
{

}

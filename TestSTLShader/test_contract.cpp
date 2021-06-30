////////////////////////
#include "Shaders/common.h"

#include "test_contract.h"
#include <vector>
#include <string>
#include <map>
#include <numeric>


export void Ctor(void*)
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

export void Dtor(void*)
{
 
}

export void Method_2(const void*)
{

}

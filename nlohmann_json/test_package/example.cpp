#include <iostream>
#include <iomanip>
#include <nlohmann/json.hpp>

int main()
{
    // create a JSON object
    nlohmann::json j = {{"pi", 3.141},
                        {"happy", true},
                        {"name", "Niels"},
                        {"nothing", nullptr},
                        {"answer", {{"everything", 42}}},
                        {"list", {1, 0, 2}},
                        {"object", {{"currency", "USD"}, {"value", 42.99}}}};

    // add new values
    j["new"]["key"]["value"] = {"another", "list"};

    // count elements
    const auto s = j.size();
    j["size"] = s;

    // pretty print with indent of 4 spaces
    std::cout << std::setw(4) << j << '\n';
}

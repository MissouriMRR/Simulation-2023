
#include <iostream>
#include <fstream>
#include "nlohmann/json.hpp"
#include <vector>
#include <iomanip>

using json = nlohmann::json;
using namespace std;

struct Coord {
    double m_lat;
    double m_long;
};

int main() {
    std::ifstream f("data/coordinates.json");
    json data = json::parse(f);

    vector<Coord> coords;

    for (auto& el : data["flight_boundary"]) {
        coords.push_back(Coord {el[0], el[1]});
    }

    for (int i = 0; i < coords.size(); i++) {
        cout << setprecision(16) << coords[i].m_lat << " " << coords[i].m_long << endl;
    } 

    return 0;
}

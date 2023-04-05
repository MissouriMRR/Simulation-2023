/*
This is a test file for potential use and adaptation to Unreal Engine later

In Unreal, this would be used to parse and represent flight parameters from
a json file (check data/coordinates.json)
*/

#pragma once

#include <fstream>
#include "nlohmann/json.hpp"
#include <vector>

using json = nlohmann::json;

struct Coord {
    double latitude;
    double longitude;
};

struct FlightParams {
    float flying_alt_agl[2];
    float flying_alt_msl[2];
    float max_error;
    Coord center;
    Coord rth;
    std::vector<Coord> flight_boundary;
    std::vector<Coord> airdrop_boundary;
};

FlightParams params_from_json(const char* filepath);

std::ostream& operator<<(std::ostream& os, const Coord& coord);
std::ostream& operator<<(std::ostream& os, const FlightParams& params);

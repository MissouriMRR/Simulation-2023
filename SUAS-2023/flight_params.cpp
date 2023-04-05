#include "flight_params.h"
#include <iomanip>

FlightParams params_from_json(const char* filepath)
{
    FlightParams params;

    std::ifstream f(filepath);
    json data = json::parse(f);

    for (auto& el : data["flight_boundary"]) {
        params.flight_boundary.push_back(Coord{ el[0], el[1] });
    }

    for (auto& el : data["air_drop_boundary"]) {
        params.airdrop_boundary.push_back(Coord{ el[0], el[1] });
    }

    params.center = Coord {data["center"][0], data["center"][1]};
    params.rth = Coord {data["RTH"][0], data["RTH"][1]};

    params.max_error = static_cast<float>(data["max_error"]);

    params.flying_alt_agl[0] = static_cast<float>(data["flying_altitude"]["agl"]["min"]);
    params.flying_alt_agl[1] = static_cast<float>(data["flying_altitude"]["agl"]["max"]);
    params.flying_alt_msl[0] = static_cast<float>(data["flying_altitude"]["msl"]["min"]);
    params.flying_alt_msl[1] = static_cast<float>(data["flying_altitude"]["msl"]["max"]);

    return params;
}

std::ostream& operator<<(std::ostream& os, const Coord& coord)
{
    os << "[" << std::setprecision(16) << coord.latitude << ", " << coord.longitude << "]";

    return os;
}

std::ostream& operator<<(std::ostream& os, const FlightParams& params)
{
    os << "{\n    flying_alt_agl: [" << params.flying_alt_agl[0] << ", " << params.flying_alt_agl[1] 
       << "],\n    flying_alt_msl: [" << params.flying_alt_msl[0] << ", " << params.flying_alt_msl[1]
       << "],\n    max_error: " << params.max_error
       << ",\n    center: " << params.center
       << ",\n    rth: " << params.rth
       << ",\n    flight_boundary: [";
    
    for (const Coord& c : params.flight_boundary)
    {
        os << "\n        " << c << ",";
    }

    os << "\n    ],\n    airdrop_boundary: [";

    for (const Coord& c : params.airdrop_boundary)
    {
        os << "\n        " << c << ",";
    }
    
    os << "\n    ]\n}";

    return os;
}
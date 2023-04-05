
#include <iostream>
#include "flight_params.h"

using namespace std;

int main() {
    FlightParams params = params_from_json("./data/coordinates.json");

    cout << params << endl;

    return 0;
}

# Unreal Source Files

This folder contains a handful of source files to be used in an Unreal 4.27 project. Ideally, these can be transferred to other Unreal projects for further development.

`Coord.h` and `Coord.cpp` contain a `FCoord` UStruct that can hold an individual pair of coordinates. It can also convert its values into Unreal Units to be used within the engine.

`FlightParams.h` and `FlightParams.cpp` aim to provide a way to store and represent test flight parameters in C++ and Blueprints. However, it may need to be converted to a UClass from a UStruct since its functions are inaccessible to Blueprints. `FlightParams` has the power to load data from a JSON file (formatted like `SUAS-2023/data/coordinates.json`).

`FileUtils.h` and `FileUtils.cpp` contain a Blueprint-compatible function that can open a file dialog/explorer and return the selected files. This function would be used to select a JSON file for `FlightParams` to load in the final simulation program.

`TestActor.h` and `TestActor.cpp` contain a test actor that shows how to load flight params using a file dialog/explorer.

`TestProject2.build.cs` is the build script used by the test project these source files were tested in. It contains the necessary dependency inclusions the other source files need to work properly.
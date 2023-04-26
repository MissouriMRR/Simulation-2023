// Fill out your copyright notice in the Description page of Project Settings.


#include "FlightParams.h"
#include "Coord.h"
#include "JsonUtilities.h"

FFlightParams::FFlightParams()
{
	Reset();
}

FFlightParams::FFlightParams(const FString& filepath)
{
	Reset();
	LoadFromJson(filepath);
}

void FFlightParams::Reset()
{
	flying_alt_agl = { 0, 0 };
	flying_alt_msl = { 0, 0 };

	max_error = 0;

	center = FCoord();
	rth = FCoord();

	flight_boundary.Empty();
	airdrop_boundary.Empty();
}

inline FCoord ArrayToCoord(const TArray<TSharedPtr<FJsonValue>>& val)
{
	return FCoord(val[0]->AsNumber(), val[1]->AsNumber());
}

void FFlightParams::LoadFromJson(const FString& path)
{
	// reset parameters
	Reset();

	FString JsonString; //Json converted to FString

	// error out if there were issues reading the file
	if (!FFileHelper::LoadFileToString(JsonString, *path)) 
	{
		UE_LOG(LogTemp, Error, TEXT("Could not load json from %s"), *path);
		return;
	}
	else
		UE_LOG(LogTemp, Log, TEXT("Loaded FlightParams json text from %s"), *path);

	//Create a json object to store the information from the json string
	//The json reader is used to deserialize the json object later on
	TSharedPtr<FJsonObject> JsonObject = MakeShareable(new FJsonObject());
	TSharedRef<TJsonReader<>> JsonReader = TJsonReaderFactory<>::Create(JsonString);

	// terminate function and log error if issue with JSON deserialization
	if (!FJsonSerializer::Deserialize(JsonReader, JsonObject) || !JsonObject.IsValid())
	{
		UE_LOG(LogTemp, Error, TEXT("Could not load json from %s"), *path);
		return;
	}
	

	//The person "object" that is retrieved from the given json file
	TSharedPtr<FJsonObject> AltitudeObject = JsonObject->GetObjectField("flying_altitude");
	TSharedPtr<FJsonObject> AGLAlt = AltitudeObject->GetObjectField("agl");
	TSharedPtr<FJsonObject> MSLAlt = AltitudeObject->GetObjectField("msl");
		
	// altitudes
	flying_alt_agl = { AGLAlt->GetNumberField("min"), AGLAlt->GetNumberField("min") };
	flying_alt_msl = { MSLAlt->GetNumberField("min"), MSLAlt->GetNumberField("min") };

	// max error
	max_error = JsonObject->GetNumberField("max_error");

	// center/rth
	center = ArrayToCoord(JsonObject->GetArrayField("center"));
	rth = ArrayToCoord(JsonObject->GetArrayField("rth"));

	// boundaries

	auto FlightBoundaries = JsonObject->GetArrayField("flight_boundary");

	for (const TSharedPtr<FJsonValue>& coord : FlightBoundaries)
		flight_boundary.Add(ArrayToCoord(coord->AsArray()));

	auto AirdropBoundaries = JsonObject->GetArrayField("air_drop_boundary");

	for (const TSharedPtr<FJsonValue>& coord : AirdropBoundaries)
		airdrop_boundary.Add(ArrayToCoord(coord->AsArray()));
}

FString FFlightParams::ToString() const
{
	// add text that doesn't require iteration
	FString output = FString::Printf(TEXT("{\n  flying_alt_agl: (%f, %f),\n  flying_alt_msl: (%f, %f),\n  max_error: %f,\n  center: %s,\n  rth: %s,"),
		flying_alt_agl.Get<0>(), flying_alt_agl.Get<1>(), flying_alt_msl.Get<0>(), flying_alt_msl.Get<1>(), max_error, *center.ToString(), *rth.ToString());

	// FLIGHT BOUNDARIES

	output += TEXT("\n  flight_boundary: [");

	// add each flight boundary coordinate to the string
	for (const FCoord& coord : flight_boundary)
		output += FString::Printf(TEXT("\n    %s,"), *coord.ToString());

	// AIRDROP BOUNDARIES

	output += TEXT("\n  ],\n  airdrop_boundary: [");

	// add each airdrop boundary coordinate to the string
	for (const FCoord& coord : airdrop_boundary)
		output += FString::Printf(TEXT("\n    %s,"), *coord.ToString());

	// close unclosed brackets
	output += TEXT("\n  ]\n}");

	return output;
}
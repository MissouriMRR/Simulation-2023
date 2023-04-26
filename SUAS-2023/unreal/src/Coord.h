#pragma once

#include "CoreMinimal.h"
#include "Coord.generated.h"

USTRUCT(BlueprintType)
struct FCoord
{
	GENERATED_BODY()

	UPROPERTY(EditAnywhere)
	double Latitude;

	UPROPERTY(EditAnywhere)
	double Longitude;

	FCoord() : Latitude(0), Longitude(0) {}
	FCoord(double Lat, double Long) : Latitude(Lat), Longitude(Long) {}

	void SetCoords(double Lat, double Long);
	void SetFromUnreal(double x, double y);
	void SetFromUnreal(FVector2D vec);
	void SetFromUnreal(FVector vec);

	FVector AsVector(int z = 0);
	FVector AsUnrealVector(int z = 0);

	FString ToString() const;

	// May be useful eventually...
	// static FCoord FromUnrealCoords();
	// static FCoord FromMetersCoords();
	// static FCoord FromFeetCoords();

};


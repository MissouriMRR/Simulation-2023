#include "Coord.h"

inline double DegreesToUnreal(double x)
{
	return x * 11113900;
}

inline double UnrealToDegrees(double x)
{
	return x / 11113900;
}

void FCoord::SetCoords(double Lat, double Long)
{
	Latitude = Lat;
	Longitude = Long;
}

void FCoord::SetFromUnreal(double x, double y)
{
	Latitude = UnrealToDegrees(x);
	Longitude = UnrealToDegrees(y);

}

void FCoord::SetFromUnreal(FVector2D vec) 
{
	SetFromUnreal(vec.X, vec.Y);
}

void FCoord::SetFromUnreal(FVector vec)
{
	SetFromUnreal(vec.X, vec.Y);
}

inline FVector FCoord::AsVector(int z)
{
	return FVector(Latitude, Longitude, z);
}

inline FVector FCoord::AsUnrealVector(int z)
{
	return FVector(DegreesToUnreal(Latitude), DegreesToUnreal(Longitude), z);
}

FString FCoord::ToString() const {
	return FString::Printf(TEXT("(%f, %f)"), Latitude, Longitude);
}
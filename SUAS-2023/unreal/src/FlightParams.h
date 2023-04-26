#pragma once

#include "CoreMinimal.h"
#include "Coord.h"
#include "FlightParams.generated.h"


USTRUCT(BlueprintType)
struct FFlightParams
{
    GENERATED_BODY()

    // properties

    //UPROPERTY(EditAnywhere)
    TTuple<float, float> flying_alt_agl;

    //UPROPERTY(EditAnywhere)
    TTuple<float, float> flying_alt_msl;

    UPROPERTY(EditAnywhere)
    double max_error;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FCoord center;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    FCoord rth;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FCoord> flight_boundary;

    UPROPERTY(EditAnywhere, BlueprintReadWrite)
    TArray<FCoord> airdrop_boundary;

    // methods

    FFlightParams();
    FFlightParams(const FString& FilePath);

    void LoadFromJson(const FString& FilePath);

    void Reset();

    FString ToString() const;
};
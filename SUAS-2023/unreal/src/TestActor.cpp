// Fill out your copyright notice in the Description page of Project Settings.


#include "TestActor.h"
#include "FlightParams.h"
#include "FileUtils.h"

// Sets default values
ATestActor::ATestActor()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = false;

}

// Called when the game starts or when spawned
void ATestActor::BeginPlay()
{
	TArray<FString> files = UFileUtils::OpenFileDialog("Select JSON", "", "", "JSON Files (*.json)|*.json");

	test = FFlightParams();

	if (files.Num() != 0)
		test.LoadFromJson(files[0]);

	GEngine->AddOnScreenDebugMessage(-1, 5.f, FColor::Red, test.ToString());
}

// Called every frame
void ATestActor::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

}


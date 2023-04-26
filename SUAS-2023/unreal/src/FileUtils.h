// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "FileUtils.generated.h"

/**
 * 
 */
UCLASS()
class TESTPROJECT2_API UFileUtils : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:

	UFUNCTION(BlueprintCallable, Category = "Files")
	static TArray<FString> OpenFileDialog(
		// The title of the file-exploring window.
		const FString& WindowTitle = "Select a file", 
		// The default path of the file explorer.
		const FString& DefaultPath = "", 
		// The default file of the file explorer.
		const FString& DefaultFile = "", 
		// The filetypes accepted by the file explorer.
		const FString& FileTypes = "All File (*.*)|*.*", 
		// Flags
		int Flags = 0
	);
	
};

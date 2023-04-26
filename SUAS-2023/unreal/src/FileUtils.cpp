// Fill out your copyright notice in the Description page of Project Settings.

#include "FileUtils.h"
#include "DesktopPlatformModule.h"

TArray<FString> UFileUtils::OpenFileDialog(const FString& WindowTitle, const FString& DefaultPath, const FString& DefaultFile, const FString& FileTypes, int Flags)
{
    IDesktopPlatform* Platform = FDesktopPlatformModule::Get();
    TArray<FString> OutFiles;

    if (Platform && Flags >= 0)
        Platform->OpenFileDialog(nullptr, WindowTitle, DefaultPath, DefaultFile, FileTypes, Flags, OutFiles);

    return OutFiles;
}
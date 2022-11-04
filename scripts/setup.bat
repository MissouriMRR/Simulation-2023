@ECHO OFF

REM server-config.json will be gitignored
REM this file is to ensure everyone easily has the correct server-config.json format in the correct location

type .\templates\server-config.lock.json > .\server-config.json
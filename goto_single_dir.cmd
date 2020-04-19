set dirname=""
set dirname=""
set /a filecount=0

echo off
:next_turn
for /D %%i in (%cd%\*) do (
     set /a filecount += 1 
     set dirname=%%i
)
goto :changedir


:changedir 
    if %filecount% == 1 (cd %dirname%) else goto :end
    set /a filecount=0
    goto :next_turn

:end
echo on

@echo off
rem Runs the Kedro pipeline and opens Kedro-Viz in the browser.
rem If you use another conda environment, change "base" below to its name.
set ENV_NAME=base

cd /d "%~dp0"
call "%USERPROFILE%\anaconda3\Scripts\activate.bat" %ENV_NAME%

kedro run
kedro viz run

pause

@echo off
REM ----------------------------------------------------------------------
REM |
REM |  admin_setup.cmd
REM |
REM |  David Brownell <db@DavidBrownell.com>
REM |      2019-04-16 21:54:19
REM |
REM ----------------------------------------------------------------------
REM |
REM |  Copyright David Brownell 2019
REM |  Distributed under the Boost Software License, Version 1.0. See
REM |  accompanying file LICENSE_1_0.txt or copy at
REM |  http://www.boost.org/LICENSE_1_0.txt.
REM |
REM ----------------------------------------------------------------------
REM Setup activites that require admin access

if not exist "%~dp0\admin_setup.reg" (
    echo ERROR: Please run Setup.cmd before executing this script.
    exit /B -1
)

echo Adding registry settings; please select "Yes" when prompted...
regedit "%~dp0\admin_setup.reg"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Unable to update the registry
    exit /B %ERRORLEVEL%
)

(
echo This file is used to communicate that admin_setup has been run and completed successfully. Please do not remove this file, as it will cause other tools to prompt you to run admin_setup.cmd again.
echo.
echo     - "admin_setup.reg"
echo.
) > "%~dp0admin_setup.complete"

echo.
echo.
echo The setup activities were successful - you may close this command prompt.
echo.
echo.

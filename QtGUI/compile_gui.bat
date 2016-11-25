for /f %%F in ('dir /b /s ".\*.ui"') do (
	call D:\Python35-32\Lib\site-packages\PyQt4\pyuic4.bat -x %%F -o %%F.py
)

@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
SET old=.ui
SET new=
for /f "tokens=*" %%f in ('dir /b *.py') do (
	Set newname=%%f
	Set newname=!newname:%old%=%new%!
	move "%%f" "!newname!"
)
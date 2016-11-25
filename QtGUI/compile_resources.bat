for /f %%F in ('dir /b /s ".\*.qrc"') do (
	call D:\Python34\Lib\site-packages\PyQt4\pyrcc4.exe -py3 %%F -o %%F_rc.py
)

@echo off
SETLOCAL ENABLEDELAYEDEXPANSION
SET old=.qrc
SET new=
for /f "tokens=*" %%f in ('dir /b *.py') do (
	Set newname=%%f
	Set newname=!newname:%old%=%new%!
	move "%%f" "!newname!"
)
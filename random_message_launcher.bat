@echo off
REM Random Message Launcher for Mom

REM Get random number 1-8
set /a num=%random% %% 8 + 1

REM Launch corresponding message
if %num%==1 start notepad "morning_surprise.txt"
if %num%==2 start notepad "afternoon_surprise.txt"
if %num%==3 start notepad "evening_surprise.txt"
if %num%==4 start notepad "love_note.txt"
if %num%==5 start notepad "motivation.txt"
if %num%==6 start notepad "silly_surprise.txt"
if %num%==7 start notepad "gratitude.txt"
if %num%==8 start notepad "weekend_surprise.txt"

@echo off
REM Time-based Message Launcher

REM Get current hour
for /f "tokens=1-2 delims=:" %%a in ('time /t') do set hour=%%a

REM Morning (6 AM - 11 AM)
if %hour% GEQ 6 if %hour% LSS 12 start notepad "morning_surprise.txt"

REM Afternoon (12 PM - 5 PM)
if %hour% GEQ 12 if %hour% LSS 17 start notepad "afternoon_surprise.txt"

REM Evening (5 PM - 11 PM)
if %hour% GEQ 17 if %hour% LSS 23 start notepad "evening_surprise.txt"

REM Late night (11 PM - 6 AM) - Love note
if %hour% GEQ 23 start notepad "love_note.txt"
if %hour% LSS 6 start notepad "love_note.txt"

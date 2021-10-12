@ECHO OFF

cls
if not exist venv/ (
    py -m venv venv 
    ECHO Virtual environment "venv" created.
) 

call .\venv\Scripts\activate

pip install -r requirements.txt

cd %~d0%~p0

set FLASK_DEBUG=1

set FLASK_APP=app_main/

set FLASK_ENV=venv

flask run
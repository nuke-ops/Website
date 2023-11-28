# nukeops.com
~~Absolute mess~~ Website made for Nukeops guild
~~I promise, one day I'll make it look like actual webside instead of some html playground~~  


## How to setup
###### Make an env and install requirements
```
python -m venv .venv
pip install -r requirements.txt
```
###### + gunicorn if you need wsgi server
```
pip install gunicorn
```
## run
### Debug
##### Linux
```
.venv/bin/python uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
##### Windows
```
.venv/scripts/python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
### Production
```
.venv/bin/python gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
```
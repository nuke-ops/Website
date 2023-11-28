# nukeops.com

#### How to deploy on linux
```
python -m venv .venv
pip install -r requirements.txt
.venv/bin/python -O -m gunicorn -k gevent -w 1 'app:create_app()'
```

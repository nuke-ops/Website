# nukeops.com

#### How to deploy on linux
```
python -m venv .venv
pip install -r requirements.txt
pip install gunicorn
.venv/bin/python -O -m gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 'app:create_app()'
```

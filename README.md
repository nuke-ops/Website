# nukeops.com
~~Absolute mess~~ Website made for Nukeops guild
~~I promise, one day I'll make it look like actual webside instead of some html playground~~  


## How to setup
###### Make an env and install requirements
```
python -m venv .venv
pip install -r requirements.txt
```
## run
#### Linux
```
.venv/bin/python -O -m daphne nukeops.asgi:application
```
#### Windows
```
.venv/scripts/python -O -m daphne nukeops.asgi:application
```

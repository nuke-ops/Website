# nukeops.com
[![CodeQL](https://github.com/nuke-ops/Website/actions/workflows/codeql-analysis.yml/badge.svg?branch=main)](https://github.com/nuke-ops/Website/actions/workflows/codeql-analysis.yml)
[![Django CI](https://github.com/nuke-ops/Website/actions/workflows/django.yml/badge.svg?branch=main)](https://github.com/nuke-ops/Website/actions/workflows/django.yml)

~~Absolute mess~~ Website made for NukeOps guild
~~I promise, one day I'll make it look like actual webside instead of some html playground~~  


## How to setup
##### Make an env and install requirements
```bash
python -m venv .venv

# Windows
".\.venv\Scripts\activate.bat"
# Linux
source .venv/bin/activate

pip install requirements.txt
```
## run
#### Debug
```
python manage.py runserver
```
#### Production
```
python -O -m daphne nukeops.asgi:application
```

## Apps

| App               | Desc                                                                                  |
| ----------------- | ------------------------------------------------------------------------------------- |
| main_page         | Main Page                                                                             |
| dice              | D&D focused dice roller                                                               |
| stream            | Bootleg stream platform                                                               |
| auth_app          | Authentication system <br> using default django auth model (for now, question mark)   |
| error_handlers    | Error handlers                                                                        |


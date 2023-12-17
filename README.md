# nukeops.com
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


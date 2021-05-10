# dynamic url Django App
A basic app where a user can create a dynamic Endpoint to inspect data in user friendly way and that endpoint is valid for an hour.

## Live App
```
Home: https://dynamicurl.herokuapp.com/
Admin: https://dynamicurl.herokuapp.com/dynamic_admin
```


## Installation
```bash
git clone https://github.com/pssukhwani/dynamic_url.git
cd ~/dynamic_url
pip install -r requirements.txt
```

## local settings:
Create Local settings file under:
```bash
cd ~/dynamic_url/dynamic_url/
touch custom_settings.py
nano custom_settings.py
```

Add the following:
```
DEBUG = True
ALLOWED_HOSTS = ["*"]
SECURE_SSL_REDIRECT = False
```
## Run Server
```bash
python manage.py runserver # Start Django Server
Home: http://localhost:8000
Admin: http://localhost:8000/dynamic_admin
```

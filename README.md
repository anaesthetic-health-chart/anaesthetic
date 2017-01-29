This is anaesthetic - an [OPAL](https://github.com/openhealthcare/opal) project.

## Setting up the applicaiton in development

also need libpq-dev


```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

To access the application, visit http://127.0.0.1:8000 in a browser, select lists, add a patient.


To view the live chart go to: http://127.0.0.1:8000/#/patient/1/anaesthetic_readings

## I want to feed data
first you need to add in session authentication, create a token header in a shell


```python
  from rest_framework.authtoken.models import Token

  token = Token.objects.create(user=YourUser)
```

for more information
http://www.django-rest-framework.org/api-guide/authentication/

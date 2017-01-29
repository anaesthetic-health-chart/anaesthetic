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
You need a token to go in http header "Authorization: Token <token goes here>" you can get a token for a user by running:

```bash
python manage.py gettoken <username>
```

This can be used with the 'anaesthetic-adaptor-vscapture' project and jakadapt.py to load data from a .csv

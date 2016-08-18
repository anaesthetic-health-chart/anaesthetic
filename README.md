This is anaesthetic - an [OPAL](https://github.com/openhealthcare/opal) project.

## Setting up the applicaiton in development

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

To access the application, visit http://127.0.0.1:8000 in a browser, select lists, add a patient.


To view the live chart go to: http://127.0.0.1:8000/#/patient/1/anaesthetic_readings

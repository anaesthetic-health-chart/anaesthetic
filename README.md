This is anaesthetic - an [OPAL](https://github.com/openhealthcare/opal) project.

To get started, run the following commands: 

```
    python manage.py syncdb --migrate
    python manage.py runserver
    
    
```

This to run it, go to http://127.0.0.1:800, select lists, add a patient. Then go to...

http://127.0.0.1:8000/#/patient/1/anaesthetic_readings

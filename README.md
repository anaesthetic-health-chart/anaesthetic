This is anaesthetic - an [OPAL](https://github.com/openhealthcare/opal) project.

## Setting up the application in development
Python and pip should already be installed however you will need to install some extra development tools to make sure everything installs without errors

On Debian/Ubuntu systems and on bash for windows type
```bash
sudo apt-get install libpq-dev
```

On RHEL/fedora use
```bash
sudo dnf install postgresql-devel python-dev rpm-build
```

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

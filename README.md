# TripConstructor

To run the project

1. Unpack the archive: `tar -xf trip_constructor.tar.gz`
2. Create virtual environment	
  `cd trip_constructor`
	`mkdir .env`
	`virtualenv .env`
5. Activate virtual environment: `source .env/bin/activate`
6. Install required packages	`pip install -r pip_requirements.txt`
7. Create database	`python manage.py syncdb`
7. Run project	`python manage.py runserver`
8. Open browser: <a href="http://127.0.0.1:8000">http://127.0.0.1:8000</a>

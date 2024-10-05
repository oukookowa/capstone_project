sv:
	python manage.py runserver

db:
	python manage.py makemigrations
	python manage.py migrate

sql:
	sudo service mysql start
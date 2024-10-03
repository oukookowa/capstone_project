sv:
	sudo service mysql start
	python manage.py runserver

db:
	python manage.py makemigrations
	python manage.py migrate


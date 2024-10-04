sv:
	sudo service mysql start
	python manage.py runserver

db:
	sudo service mysql start
	python manage.py makemigrations
	python manage.py migrate


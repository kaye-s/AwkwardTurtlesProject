remigrate:
	rm db.sqlite3
	rm -rf ./TAScheduler/migrations
	mkdir ./TAScheduler/migrations
	cd ./TAScheduler/migrations && touch "__init__.py"
	python3 manage.py makemigrations
	python3 manage.py migrate
	
remigrate:
	rm db.sqlite3
	rm -rf ./TAScheduler/migrations
	mkdir ./TAScheduler/migrations
	cd ./TAScheduler/migrations && touch "__init__.py"

migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate
	34:48
	
	
	
	2
	
	
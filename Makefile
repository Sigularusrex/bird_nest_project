venv:
	source venv/bin/activate

get_started:
	pip install -r requirements.txt
	python manage.py makemigrations
	python manage.py migrate
	python manage.py createsuperuser

load_data_from_source_data_folder:
	python manage.py load_source_data source_data

enrich_source_data_from_csv:
	python manage.py enrich_source_data_from_csv source_data/data_enrichment.csv

seed_db:
	make load_data_from_source_data_folder
	make enrich_source_data_from_csv

start:
	python manage.py shell_plus --lab
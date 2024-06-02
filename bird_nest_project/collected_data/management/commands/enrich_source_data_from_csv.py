# image_metadata/management/commands/enrich_metadata.py
import csv
import json
from collections import defaultdict
from django.core.management.base import BaseCommand
from bird_nest_project.collected_data.models import PlottedData
from tqdm import tqdm


class Command(BaseCommand):
    help = "Enrich image metadata with data from a CSV file and store it in the enriched_data column"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")

    def handle(self, *args, **options):
        csv_file = options["csv_file"]
        self.enrich_metadata(csv_file)

    def enrich_metadata(self, csv_file):
        # Read the CSV file and create a mapping of IDs to group names
        with open(csv_file, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in tqdm(reader):
                updated_rows = PlottedData.objects.filter(group_name=row["id"]).update(
                    enriched_data=row
                )
                if updated_rows == 0:
                    print(f"No data found for group {row['id']}")

# image_metadata/management/commands/enrich_metadata.py
import csv
import os
from django.core.management.base import BaseCommand
from bird_nest_project.collected_data.models import PlottedData
from tqdm import tqdm
import gpxpy
import datetime


class Command(BaseCommand):
    help = "Enrich image metadata with data from a CSV file and store it in the enriched_data column"

    def add_arguments(self, parser):
        parser.add_argument("csv_file", type=str, help="Path to the CSV file")

    def handle(self, *args, **options):
        folder_path = options["folder_path"]

        folders = self.find_subfolders(folder_path)
        images = PlottedData.objects.all()
        for image in images:
            target_time = image.created_at
            for folder in tqdm(folders):
                coordinates = self.get_coordinates_at_time(folder, target_time)
                if coordinates is not None:
                    image.strava_latitude = coordinates[0]
                    image.strava_longitude = coordinates[1]
                    image.save()
                    break
            if coordinates:
                print(
                    "Coordinates at {}: Latitude = {}, Longitude = {}".format(
                        target_time, coordinates[0], coordinates[1]
                    )
                )
            else:
                print("Coordinates at {} not found.".format(target_time))

    def find_subfolders(self, folder_path: str):
        subfolders = []
        for root, dirs, files in os.walk(folder_path):
            for dir in dirs:
                subfolders.append(os.path.join(root, dir))
        return subfolders

    def get_coordinates_at_time(folder_path: str, target_time: datetime) -> dict:
        for filename in os.listdir(folder_path):
            if filename.endswith(".gpx"):
                # Load GPX file
                with open(filename, "r") as gpx_file:
                    gpx = gpxpy.parse(gpx_file)

                # Iterate through tracks, segments, and points to find coordinates at the specified time
                for track in gpx.tracks:
                    for segment in track.segments:
                        for point in segment.points:
                            if point.time and point.time == target_time:
                                return point.latitude, point.longitude

                # If coordinates are not found at the specified time, return None
                return None

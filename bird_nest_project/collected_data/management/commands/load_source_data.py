# image_metadata/management/commands/extract_metadata.py
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from django.core.management.base import BaseCommand
from bird_nest_project.collected_data.repositories import PlottedDataRepository
from tqdm import tqdm


class Command(BaseCommand):
    help = "Extract metadata from images in a folder and store it in the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "folder_path", type=str, help="Path to the folder containing images"
        )

    def handle(self, *args, **options):
        folder_path = options["folder_path"]
        plotted_data = []
        print("Loading source data")
        print("1. Discover datapoints grouped by folder")
        folders = self.find_subfolders(folder_path)
        print(f"Found {len(folders)} subfolders")
        for folder in tqdm(folders):
            group_name = folder.split("/")[1]
            group_data = self.extract_metadata_from_images(
                folder_path=folder, group_name=group_name
            )
            plotted_data.extend(group_data)
        print(f"found {len(plotted_data)} data points")
        print(plotted_data)
        print("2. Saving data to the database")
        PlottedDataRepository().seed(plotted_data)

    def get_exif_data(self, image) -> dict:
        exif_data = {}
        info = image._getexif()
        if info:
            for tag, value in info.items():
                decoded_tag = TAGS.get(tag, tag)
                if decoded_tag == "GPSInfo":
                    gps_info = {}
                    for t in value:
                        sub_decoded_tag = GPSTAGS.get(t, t)
                        gps_info[sub_decoded_tag] = value[t]
                    exif_data[decoded_tag] = gps_info
                else:
                    exif_data[decoded_tag] = value
        return exif_data

    def find_subfolders(self, folder_path):
        subfolders = []
        for root, dirs, files in os.walk(folder_path):
            for dir in dirs:
                subfolders.append(os.path.join(root, dir))
        return subfolders

    def extract_metadata_from_images(self, folder_path: str, group_name: str) -> list:
        group_data = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                file_path = os.path.join(folder_path, filename)
                with Image.open(file_path) as img:
                    format = img.format
                    exif_data = self.get_exif_data(img)
                    latitude = None
                    longitude = None
                    if "GPSInfo" in exif_data:
                        gps_info = exif_data["GPSInfo"]
                        if "GPSLatitude" in gps_info and "GPSLongitude" in gps_info:
                            lat_deg, lat_min, lat_sec = gps_info["GPSLatitude"]
                            lon_deg, lon_min, lon_sec = gps_info["GPSLongitude"]
                            latitude = (lat_deg + lat_min / 60.0 + lat_sec / 3600.0) * (
                                -1 if gps_info["GPSLatitudeRef"] == "S" else 1
                            )
                            longitude = (
                                lon_deg + lon_min / 60.0 + lon_sec / 3600.0
                            ) * (-1 if gps_info["GPSLongitudeRef"] == "W" else 1)
                    group_data.append(
                        {
                            "file_path": file_path,
                            "format": format,
                            "latitude": latitude,
                            "longitude": longitude,
                            "group_name": group_name,
                        }
                    )
        return group_data

from rest_framework import serializers
from bird_nest_project.collected_data.models import PlottedData


class PlottedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlottedData
        fields = [
            "id",
            "group_name",
            "file_path",
            "format",
            "latitude",
            "longitude",
            "enriched_data",
            "created_at",
            "strava_latitude",
            "strave_longitude",
        ]

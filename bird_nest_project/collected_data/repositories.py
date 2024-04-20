from bird_nest_project.collected_data.models import PlottedData
from bird_nest_project.collected_data.serializers import PlottedDataSerializer


class PlottedDataRepository:
    @classmethod
    def seed(cls, seed_data: list[dict]) -> list[PlottedData]:
        serializer = PlottedDataSerializer(data=seed_data, many=True)
        serializer.is_valid(raise_exception=True)  # Validate the data
        serializer.save()

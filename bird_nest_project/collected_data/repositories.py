from bird_nest_project.collected_data.models import PlottedData
from bird_nest_project.collected_data.serializers import PlottedDataSerializer


class PlottedDataRepository:
    def seed(cls, seed_data: list[dict]) -> list[PlottedData]:
        existing_file_paths = PlottedData.objects.values_list('file_path', flat=True)
        new_data = [data for data in seed_data if data['file_path'] not in existing_file_paths]
        
        if not new_data:
            return []  # If no new data to save, return empty list
        
        serializer = PlottedDataSerializer(data=new_data, many=True)
        serializer.is_valid(raise_exception=True)  # Validate the data
        serializer.save()
        return serializer.instance
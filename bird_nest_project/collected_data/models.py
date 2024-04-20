from django.db import models


class PlottedData(models.Model):
    group_name = models.CharField(max_length=100, db_index=True)
    file_path = models.CharField(max_length=512)
    format = models.CharField(max_length=10)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    enriched_data = models.JSONField(null=True, blank=True)

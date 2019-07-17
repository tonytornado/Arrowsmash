from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from Scores.models import Score, SongChart


class SongChartResource(resources.ModelResource):
    class Meta:
        model = SongChart


class SongChartAdmin(ImportExportModelAdmin):
    resource_class = SongChartResource


admin.site.register(Score)
admin.site.register(SongChart, SongChartAdmin)

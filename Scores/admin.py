from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from Scores.models import Score, Song, Mix


class SongResource(resources.ModelResource):
    class Meta:
        model = Song


class SongAdmin(ImportExportModelAdmin):
    resource_class = SongResource


admin.site.register(Score)
admin.site.register(Song, SongAdmin)
admin.site.register(Mix)

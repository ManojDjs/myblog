from django.contrib import admin

# Register your models here.
from .models import Post,Location,Member
admin.site.register(Post)
admin.site.register(Location)
from import_export.admin import ImportExportModelAdmin
@admin.register(Member)
class MemberAdmin(ImportExportModelAdmin):
    list_display = ("firstname", "lastname", "email", "birth_date")
    pass
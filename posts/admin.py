from django.contrib import admin

# Register your models here.
from .models import Post,Location
admin.site.register(Post)
admin.site.register(Location)

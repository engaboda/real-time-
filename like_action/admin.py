from django.contrib import admin
from .models import Image, Like

# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    save_as = True
    
admin.site.register(Image, ImageAdmin)
admin.site.register(Like)
from django.contrib import admin
from .models import Image,JSONFile, JSONModelQP# Register your models here.


class StudentAdmin(admin.ModelAdmin):
    list_display = ['image']
admin.site.register(Image, StudentAdmin)


class JsonAdmin(admin.ModelAdmin):
    list_display = ['file']
admin.site.register(JSONFile,JsonAdmin)


class JsonAdmin(admin.ModelAdmin):
    list_display = ['file']
admin.site.register(JSONModelQP,JsonAdmin)
from django.contrib import admin
from mainchat.models import Chating
# Register your models here.
@admin.register(Chating)
class chating(admin.ModelAdmin):
    list_display=['content','username']
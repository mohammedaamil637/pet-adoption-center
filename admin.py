from django.contrib import admin
from .models import Pet

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'animal_type', 'breed', 'status', 'created_at')
    list_filter = ('animal_type', 'status')
    search_fields = ('name', 'breed')

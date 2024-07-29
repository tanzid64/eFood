from django.contrib import admin
from .models import Category, FoodItem
# Register your models here.
class CategoryAdim(admin.ModelAdmin):
  prepopulated_fields = {'slug':('category_name',)}
  list_display = ('category_name', 'vendor', 'created_at')
  search_fields = ('category_name', 'vendor__vendor_name')

class FoodItemAdmin(admin.ModelAdmin):
  prepopulated_fields = {'slug':('food_title',)} 
  list_display = ('food_title', 'category', 'vendor', 'price', 'is_available')
  search_fields = ('food_title', 'category__category_name', 'vendor__vendor_name', 'price')
  list_filter = ('is_available',)

admin.site.register(Category, CategoryAdim)
admin.site.register(FoodItem, FoodItemAdmin)
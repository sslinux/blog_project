from django.contrib import admin
from .models import Post,Tag,Category

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_time', 'modified_time', 'category', 'author']
    list_per_page = 10
    list_filter = ['category']


admin.site.register(Post,PostAdmin)
admin.site.register(Tag)
admin.site.register(Category)
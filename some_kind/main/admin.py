from django.contrib import admin
from main.models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug':('name',)}

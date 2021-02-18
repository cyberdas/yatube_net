from django.contrib import admin
from .models import Post, Group

class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author")
    search_fields = ("text",)
    list_filter = ("pub_date",)  
    empty_value_display = '-пусто-'
    def group_title(self, obj):
        return obj.group.title
    group_title.short_description = "Group"
    
class GroupAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "description")
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)

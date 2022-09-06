from django.contrib import admin
from .models import User, Post

'''-----------Custom user model register here------------'''

admin.site.register(User)
# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title','author','content','created_on',"updated_on")

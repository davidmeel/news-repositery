from django.contrib import admin
from news.models import *

admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(PostFiles)
admin.site.register(PostComment)
admin.site.register(PostFavorites)
from django.contrib import admin
from .models import Post

# allows for models like Post to be accessed through Admin site
admin.site.register(Post)


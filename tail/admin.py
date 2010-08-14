from django.contrib import admin

from tail.models import Server, FilePath

admin.site.register([Server, FilePath])
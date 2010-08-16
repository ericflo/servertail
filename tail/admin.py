from django.contrib import admin

from tail.models import ServerTail, FrontPage

class FrontPageAdmin(admin.ModelAdmin):
    list_display = ('server_tail', 'date')
    date_hierarchy = 'date'
    raw_id_fields = ('server_tail',)

class ServerTailAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'port', 'username', 'user', 'date_created')
    search_fields = ('hostname', 'username', 'path')
    date_hierarchy = 'date_created'
    raw_id_fields = ('user',)

admin.site.register(ServerTail, ServerTailAdmin)
admin.site.register(FrontPage, FrontPageAdmin)
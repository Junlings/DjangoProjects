from models import clients, UserProfile
from django.contrib import admin


admin.site.register(UserProfile)
admin.site.register(clients)#,ClientInline)

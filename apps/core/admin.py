from django.contrib import admin
from .models import LoginRecord, LoginAttempt


admin.site.register(LoginRecord)
admin.site.register(LoginAttempt)

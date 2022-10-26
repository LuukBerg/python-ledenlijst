from django.contrib import admin
from home.models import Member

# Register your models here.


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass

from django.contrib import admin
from .models import User_form, AttendanceRecord

# Register your models here.
@admin.register(User_form)
class userAdminModel(admin.ModelAdmin):
    list_display= ["id","first_name", "last_name"]
@admin.register(AttendanceRecord)
class AttendanceRecordAdminModel(admin.ModelAdmin):
    list_display = ["date"]


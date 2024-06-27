from django.urls import path
from .views import register_person, attendanceRecord, person_detail,compare_images,mark_attendance_success, attendance_record, user_signup, user_login,logout_user, front_page, delete_person



urlpatterns = [
    path("", front_page, name="front_page"),
    path("register/",register_person, name="register_person"),
    path("home/", attendanceRecord, name="attendanceRecord"),
    path("detail/<int:id>", person_detail, name="person_detail"),
    path("attendance_record/",attendance_record,name='attendance_record'),
    path('compare_images/', compare_images, name='compare_images'),
    path('attendance/success/<int:pk>/', mark_attendance_success, name='mark_attendance_success'),
    path("user_signupForm/",user_signup, name="user_signupForm"),
    path("login/", user_login, name="user_login"),  
    path("logout/", logout_user, name="logout"),  
    path("del/<int:id>", delete_person, name="delete"),
   
]


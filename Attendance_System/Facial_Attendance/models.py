from django.db import models

# Create your models here.


class User_form(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    face_embedding = models.BinaryField()  # Store the face embedding as binary data

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    
class AttendanceRecord(models.Model):
    user = models.ForeignKey(User_form, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time_in = models.TimeField(auto_now_add=True)
    time_out = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"AttendanceRecord for {self.user} on {self.date}"
    






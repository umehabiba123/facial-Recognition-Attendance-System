from django.shortcuts import render, redirect
from .forms import PersonForm, SignUpForm, LoginForm
from .models import AttendanceRecord, User_form
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
import cv2
import face_recognition
import numpy as np
from django.http import HttpResponse, HttpResponseRedirect
import winsound
from datetime import datetime
from django.http import JsonResponse
import datetime
from django.shortcuts import render, get_object_or_404


def front_page(request): 
    return render(request,"frontpage.html")


def register_person(request):
    form = PersonForm(request.POST or None,request.FILES or None)
    if request.method == "POST":
        if form.is_valid():  
            form.save()
            messages.success(request, 'User registered successfully.')
            return redirect('/home/')
    return render(request, "create_form.html", {"form": form})

def user_signup(request):

    if request.method == 'POST':
            
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulation !! You have become an author')
            form.save()
            return redirect('/home/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
    




def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                user_name = form.cleaned_data['username']  
                user_password =  form.cleaned_data['password']
                user = authenticate(username=user_name, password=user_password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'LoggedIn successfully')
                    return HttpResponseRedirect('/home/')
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        return HttpResponseRedirect('/home/')
    
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/login/")

def attendanceRecord(request):
    portal = User_form.objects.all()

    Portal = {"portal":portal}
    return render(request, "home.html", Portal)
            
def person_detail(request, id):
    person_detail = User_form.objects.get(pk = id)
    person_detail = {"person":person_detail}
    return render(request, "detail.html", person_detail)

def delete_person(request,pk):
    delete_object = User_form.object.get(pk=pk)
    delete_object.delete()
    return render("/")

register_person


def mark_attendance_success(request, pk):


    persons = User_form.objects.get(pk=pk)
    
    user= persons
    attendance_record, created = AttendanceRecord.objects.get_or_create(
                        user=user,
                        date=datetime.date.today(),
                        defaults={'time_in': datetime.datetime.now().time()})
    if not created:
        attendance_record.time_out = datetime.datetime.now().time()
        attendance_record.save()
        
    print(attendance_record)
   
    # AttendanceRecord.user = get_object_or_404(User, first_name=user_att) 
    
    # attendance_record = get_object_or_404(AttendanceRecord, user=AttendanceRecord.user)
   

    # attendance_record = get_object_or_404(AttendanceRecord, user=pk)

    user = attendance_record.user
    
    return render(request,'record.html', {'user': user, 'attendance_record': attendance_record})






def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return None
    print(cap)

    ret, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()

    if ret:
        return frame
    else:
        print("Error: Could not read frame from webcam.")
        return None




def encode_database_images():
    encoded_images = []
    persons = User_form.objects.all()
    
    for person in persons:
        print(person)
        image_path = person.profile_picture.path
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            encoded_images.append((person.first_name,person.pk, encodings[0]))
    
    return encoded_images

def compare_faces(live_image, encoded_images):
    live_encodings = face_recognition.face_encodings(live_image)

    if not live_encodings:
        print("No faces found in the live image.")
        return []

    live_encoding = live_encodings[0]
    results = []
    
    for name, pk, db_encoding in encoded_images:
        match = face_recognition.compare_faces([db_encoding], live_encoding)
        distance = face_recognition.face_distance([db_encoding], live_encoding)
        if match[0]:
            results.append((name, pk, distance[0]))
    
    # Sort results by distance
    results.sort(key=lambda x: x[2])
    return results



def compare_images(request):
    if request.method == 'POST':
        # Capture the live image from the webcam
        live_image = capture_image()
        if live_image is None:
            return JsonResponse({'error': 'Failed to capture image'}, status=500)

        # Encode database images
        encoded_images = encode_database_images()
        if not encoded_images:
            return JsonResponse({'error': 'No images encoded from the database'}, status=500)

        # Compare the live image to the database images
        results = compare_faces(live_image, encoded_images)
        if results:
            print("hello2",results)
            user_id = results[0][1]
            print(user_id)
            return redirect('mark_attendance_success', pk=user_id)
            # return render(request,"success.html")
        else:
            return HttpResponse("unSuccessful")
    return render(request, 'compare_images.html')

def attendance_record(request):
    attendance_records = AttendanceRecord.objects.all()
    records_and_users = [(record, record.user) for record in attendance_records]
    return render(request,"attendance_record.html", {"records_and_users" : records_and_users})


def delete_person(request,id):
    person = User_form.objects.get(pk=id)
    person.delete()
    return redirect("/home")
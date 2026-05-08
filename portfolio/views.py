from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail

# Create your views here.

# def home(request):
#     return render(request, "home.html")


# def login_view(request):
#     if request.method == "POST":
#         email = request.POST.get("email")

#         user, created = User.objects.get_or_create(username=email, email=email)

#         otp = generate_otp()
#         OTP.objects.create(user=user, otp=otp)

#         send_mail(
#             "Your OTP Code",
#             f"Your OTP is {otp}",
#             "your_email@gmail.com",
#             [email],
#         )

#         request.session['user_id'] = user.id
#         return redirect('verify_otp')

#     return render(request, "login.html")


# def verify_otp(request):
#     if request.method == "POST":
#         otp_input = request.POST.get("otp")
#         user_id = request.session.get("user_id")

#         otp_obj = OTP.objects.filter(user_id=user_id).last()

#         if otp_obj and otp_obj.otp == otp_input:
#             return redirect('home')

#     return render(request, "verify_otp.html")



def home(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "")
        # home form might just have 'name' instead of first/last, check this!
        # wait, let me just look at the template first. I'll just use 'first_name' and 'email' and 'message' to match contact.
        first_name = request.POST.get("first_name", "")
        email = request.POST.get("email", "")
        message = request.POST.get("message", "")
        
        Contact.objects.create(
            first_name=first_name,
            email=email,
            message=message
        )
        messages.success(request, "Your message has been sent successfully!")
        return redirect('home')
    return render(request, 'home.html')
def about(request):    return render(request, 'about.html')
def projects(request): return render(request, 'projects.html')
from django.contrib import messages
from .models import Contact

def contact(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        email = request.POST.get("email", "")
        subject = request.POST.get("subject", "")
        message = request.POST.get("message", "")
        
        Contact.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            subject=subject,
            message=message
        )
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')
        
    return render(request, 'contact.html')
import ssl
import smtplib
from email.mime.text import MIMEText
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.conf import settings
from .models import OTP
from accounts.utils import generate_otp
from django.contrib import messages
from django.utils import timezone
import datetime


def send_otp_email(to_email, otp):
    msg = MIMEText(f"Your OTP is: {otp}\n\nThis OTP is valid for 10 minutes.")
    msg['Subject'] = 'Your OTP Code'
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = to_email

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
        server.ehlo()
        server.starttls(context=context)
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.EMAIL_HOST_USER, [to_email], msg.as_string())


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if not email:
            messages.error(request, "Email is required")
            return redirect('login')

        user, created = User.objects.get_or_create(username=email, email=email)
        otp = generate_otp()
        OTP.objects.create(user=user, otp=otp)

        try:
            send_otp_email(email, otp)
            messages.success(request, f"OTP sent to {email}")
        except Exception as e:
            print(f"\n{'='*40}")
            print(f"[FALLBACK] OTP for {email}: {otp}")
            print(f"Error: {e}")
            print(f"{'='*40}\n")
            messages.warning(request, "Email failed — check terminal for OTP.")

        request.session['user_id'] = user.id
        return redirect('verify_otp')

    return render(request, "login.html")


def verify_otp(request):
    if request.method == "POST":
        otp_input = request.POST.get("otp")
        user_id = request.session.get("user_id")

        if not user_id:
            messages.error(request, "Session expired. Please login again.")
            return redirect('login')

        otp_obj = OTP.objects.filter(user_id=user_id).last()
        expiry_time = timezone.now() - datetime.timedelta(minutes=10)

        if otp_obj and otp_obj.created_at >= expiry_time and otp_obj.otp == otp_input:
            user = User.objects.get(id=user_id)
            login(request, user)
            OTP.objects.filter(user=user).delete()
            return redirect('home')
        elif otp_obj and otp_obj.created_at < expiry_time:
            messages.error(request, "OTP expired. Please request a new one.")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "verify_otp.html")
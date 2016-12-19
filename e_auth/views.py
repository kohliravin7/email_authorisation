from django.shortcuts import render, redirect, get_object_or_404
from e_auth.forms import UserCreation
from django.core.signing import Signer
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from e_auth.models import UserProfile

# Create your views here.


def SignUp(request):
    if request.user.is_authenticated:
        return redirect("/home/")
    registration_form = UserCreation()
    if request.POST:
        form = registration_form(request.POST)
    if form.is_valid():
        data={}
        data["username"] = request.POST['username']
        data["password"] = request.POST["password"]
        data["email"] = request.POST["email"]
        signer = Signer(salt=data["email"])
        data["activation-key"] = signer.sign(data["username"])
        now = datetime.now()
        data["expiry"] = now + timedelta(hours=36)
        form.sendEmail(data)
        form.save()
        return redirect("/home/")
    else:
        render(request, "/signup/")
    return render(request, "/signup/")


def activation(request, key):
    profile = get_object_or_404(User, activation_key=key)
    if profile.user.is_active:
        if datetime.now() > profile.key_expires:
            return render(request, '/activation-new/' ,{"message" : "Activation Expired Resending new mail"})
        else:  # Activation successful
            profile.user.is_active = True
            profile.user.save()
            message = "Successfully Registered"

    # If user is already active, simply display error message
    else:
        message = "Account already active"
    return render(request, '/activation', {"message": message})


def new_activation_link(request, user_id):
    form = UserCreation()
    data={}
    user = User.objects.get(id=user_id)
    if user is not None and not user.is_active:
        data['username']=user.username
        data['email']=user.email

        signer = Signer(salt=data["email"])
        data["activation-key"] = signer.sign(data["username"])

        profile = UserProfile.objects.get(user=user)
        profile.activation_key = data['activation_key']
        profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(hours=36), "%Y-%m-%d %H:%M:%S")
        profile.save()

        form.sendEmail(data)

    return redirect('home')

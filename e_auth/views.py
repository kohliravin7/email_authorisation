from django.shortcuts import render, redirect, get_object_or_404
from e_auth.forms import UserCreation
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from e_auth.models import UserProfile
import hashlib,random
# Create your views here.


def signup(request):
    if request.user.is_authenticated:
        return redirect("/auth/home/")
    if request.POST:
        form = UserCreation(request.POST)
        if form.is_valid():
            data = {}
            data["username"] = form.cleaned_data['username']
            data["password"] = request.POST.get('password')
            data["email"] = request.POST.get('email')
            # signer = Signer(salt=data["email"])
            # data["activation-key"] = signer.sign(data["username"])
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
            usernamesalt = data['username']
            if isinstance(usernamesalt, unicode):
                usernamesalt = usernamesalt.encode('utf8')
            data['activation_key'] = hashlib.sha1(salt + usernamesalt).hexdigest()

            now = datetime.now()
            data["expiry"] = now + timedelta(hours=36)
            form.sendEmail(data)
            form.save(data)
            return redirect("/auth/home/")
        else:
            form = UserCreation()
            render(request, "signup.html", {"form": form})
    form = UserCreation()
    return render(request, "signup.html", {"form": form})


def activation(request):
    key = request.GET.get("key")
    profile = UserProfile.objects.filter(activation_key=key)
    profile = profile.get()
    if profile.user.is_active is not True:
        if timezone.now() > profile.expiry_date:
            return render(request, '/activation-new/?userid=%s' % profile.user_id, {"message" : "Activation Expired Resending new mail"})
        else:  # Activation successful
            profile.user.is_active = True
            profile.user.save()
            success = True
            message = "Successfully Registered"

    # If user is already active, simply display error message
    else:
        message = "Account already active"
        success = False
    return render(request, 'activation.html', {"message": message, "success": success})


def new_activation_link(request):
    user_id = request.GET.get("userid")
    form = UserCreation()
    data={}
    user = User.objects.get(id=user_id)
    if user is not None and not user.is_active:
        data['username']=user.username
        data['email']=user.email

        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        usernamesalt = data['username']
        if isinstance(usernamesalt, unicode):
            usernamesalt = usernamesalt.encode('utf8')
        data['activation_key'] = hashlib.sha1(salt + usernamesalt).hexdigest()

        profile = UserProfile.objects.get(user=user)
        profile.activation_key = data['activation_key']
        profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(hours=36), "%Y-%m-%d %H:%M:%S")
        profile.save()

        form.sendEmail(data)

    return redirect('/home/')

def home(request):
    return render(request, 'home.html')

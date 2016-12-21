from django.shortcuts import render, redirect
from e_auth.forms import UserCreation
from django.utils import timezone
from e_auth.models import UserProfile
# from e_auth.tasks import sendEmail
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from email_authorisation import generate_key, save
from django.contrib.auth.models import User
# Create your views here.


def signup(request):
    if request.user.is_authenticated and not request.user.is_anonymous():
        return redirect("/auth/home/")
    if request.POST:
        form = UserCreation(request.POST)
        if form.is_valid():
            data={}
            data["username"] = form.cleaned_data['username']
            data["password"] = request.POST.get('password')
            data["email"] = request.POST.get('email')
            # signer = Signer(salt=data["email"])
            # data["activation-key"] = signer.sign(data["username"])
            generate_key(request.user, data)
            save(data)
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
            return render(request, '/activation-new/?userid=%s' % profile.user_id, {"message": "Activation Expired Resending new mail"})
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


# def new_activation_link(request):
#     user_id = request.GET.get("userid")
#     form = UserCreation()
#     data={}
#     user = User.objects.get(id=user_id)
#     if user is not None and not user.is_active:
#         data['username']=user.username
#         data['email']=user.email
#
#         salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
#         usernamesalt = data['username']
#         if isinstance(usernamesalt, unicode):
#             usernamesalt = usernamesalt.encode('utf8')
#         data['activation_key'] = hashlib.sha1(salt + usernamesalt).hexdigest()
#
#         profile = UserProfile.objects.get(user=user)
#         profile.activation_key = data['activation_key']
#         profile.key_expires = datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(hours=36), "%Y-%m-%d %H:%M:%S")
#         profile.save()
#         if not request.user.is_active:
#             t = threading.Thread(target=form.sendEmail, args=[data], kwargs={})
#             t.setDaemon(True)
#             t.start()
#         # tasks.sendEmail.delay(data)
#
#     return redirect('/auth/home/')

def deactivate(request):
    user = User.objects.get(username=request.GET["username"])
    user.userprofile.delete()
    user.delete()
    return redirect('/auth/signup/')


def home(request):
    return render(request, 'home.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/auth/signup/')

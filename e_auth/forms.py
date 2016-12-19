from django import forms
from django.contrib.auth.models import User
from e_auth.models import UserProfile
from django.core.mail import send_mail
# form for user creation


class UserCreation(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Username'}), max_length=30, min_length=3)
    # , validators=[isValidUsername, validators.validate_slug])
    email = forms.EmailField(label="", widget=forms.EmailInput(
        attrs={'placeholder': 'Email'}), max_length=100, error_messages={'invalid': ("Invalid Email.")})
    # , validators=[isValidEmail])
    password1 = forms.CharField(label="", max_length=50, min_length=6, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ("username", 'password', 'email')
    def save(self, data):
        user = User.objects.create_user(data["username"], data["email"], data["password"])
        user.is_active = False
        user.save()
        userProfile = UserProfile()
        userProfile.user = user
        userProfile.activation_key = data["activation_key"]
        userProfile.expiry_date = data["expiry"]
        userProfile.save()

    def sendEmail(self, data):
        activation_link = 'http://127.0.0.1:8000/auth/activate/?key=%s' % data["activation_key"]
        email = data["email"]
        body = "Please press the following link to activate your account:"
        body += "\n %s" % activation_link
        send_mail("Activation link for %s" % data["username"], from_email='kohliravin7@gmail.com', message=body, recipient_list=[email], fail_silently=False)

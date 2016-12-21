from datetime import datetime, timedelta
import hashlib,random
import threading
from django.contrib.auth.models import User
from e_auth.models import UserProfile
from django.core.mail import send_mail

HOST_URL = 'http://127.0.0.1:8000/'
EMAIL_SENDER = 'testing.activation7@gmail.com'
EMAIL_BODY = "Dear %s, \n Thank you for signing up with us. Please press the following link to activate " \
             "your account:\n%s" \
             "\n To deactivate\n %s"


def generate_key(user, data):
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    usernamesalt = data['username']
    if isinstance(usernamesalt, unicode):
        usernamesalt = usernamesalt.encode('utf8')
    data['activation_key'] = hashlib.sha1(salt + usernamesalt).hexdigest()
    now = datetime.now()
    data["expiry"] = now + timedelta(hours=36)
    # tasks.sendEmail.delay(data)
    if not user.is_active:
        t = threading.Thread(target=sendEmail, args=[data], kwargs={})
        t.setDaemon(True)
        t.start()
    # return data


def save(data):
    user = User.objects.create_user(data["username"], data["email"], data["password"])
    user.is_active = False
    user.save()
    userProfile = UserProfile()
    userProfile.user = user
    userProfile.activation_key = data["activation_key"]
    userProfile.expiry_date = data["expiry"]
    userProfile.save()


def sendEmail(data):
    print "email sent"
    activation_link = '%sauth/activate/?key=%s' % (HOST_URL, data["activation_key"])
    deactivation_link = '%sauth/deactivate/?username=%s' % (HOST_URL, data["username"])
    email = data["email"]
    send_mail("Activation link for %s" % data["username"], from_email=EMAIL_SENDER, message=EMAIL_BODY % (data["username"], activation_link, deactivation_link),
              recipient_list=[email], fail_silently=False)

# from __future__ import absolute_import, unicode_literals
# from .celery import app
# from django.core.mail import send_mail
#
# HOST_URL = 'http://127.0.0.1:8000/'
# EMAIL_SENDER = 'testing.activation7@gmail.com'
#
#
# @app.task
# def sendEmail(data):
#     print "email sent"
#     activation_link = '%sauth/activate/?key=%s' % (HOST_URL, data["activation_key"])
#     email = data["email"]
#     body = "Please press the following link to activate your account:"
#     body += "\n %s" % activation_link
#     send_mail("Activation link for %s" % data["username"], from_email=EMAIL_SENDER, message=body,
#               recipient_list=[email], fail_silently=False)
#

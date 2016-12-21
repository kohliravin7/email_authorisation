# from __future__ import absolute_import, unicode_literals
# from celery import Celery
#
#
# app = Celery('app_email_async',
#              broker='amqp://guest:guest@localhost:5672//',
#              backend='amqp://',
#              include=['e_auth.tasks'])
#
# # Optional configuration, see the application user guide.
# app.conf.update(
#     result_expires=3600,
# )
#
# if __name__ == '__main__':
#     app.start()

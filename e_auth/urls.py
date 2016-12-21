from django.conf.urls import url
from e_auth.views import *
app_name = "e_auth"
urlpatterns = [
    url(r"^signup/$", signup),
    url(r"^activate/$", activation),
    # url(r"^activation-new/$", new_activation_link),
    url(r'^home/$', home),
    url(r'^logout/$', user_logout),
    url(r'^deactivate/$', deactivate)
]

from django.conf.urls import url
from .views import FileView
urlpatterns = [
    url(r'^upload/$', FileView.as_view(), name='file-upload'),
]

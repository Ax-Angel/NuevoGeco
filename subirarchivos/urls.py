from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^upload/$', DocumentView.as_view(), name='file-upload'),
    url(r'^registro-usuario/$', CreateUserView.as_view(), name='register-user'),
    url(r'^crear-proyecto-normal/$', NormalProjectView.as_view(), name='normal-project-creation'),
    url(r'^crear-md-proyecto-nor/$', NormalMetadataView.as_view(), name='crear-md-proyecto-nor'),
    url(r'^crear-proyecto-paralelo/$', ParallelProjectView.as_view(), name='parallel-project-creation'),
    url(r'^crear-md-proyecto-par/$', ParallelMetadataView.as_view(), name='crear-md-proyecto-par'),
    url(r'^rel-doc-metadato/$', DocNormalMetaRelationView.as_view(), name='rel-doc-metadato'),
    url(r'^rel-paralelo/$', ParallelRelationView.as_view(), name='rel-paralelo'),
    url(r'^rel-paral-rel-md/$', ParallelRelationView.as_view(), name='rel-paral-rel-md'),
]

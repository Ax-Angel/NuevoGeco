from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^upload1/$', DocumentView.as_view(), name='file-upload'),
    url(r'^registro-usuario/$', CreateUserView.as_view(), name='register-user'),
    url(r'^crear-proyecto-normal/$', NormalProjectView.as_view(), name='normal-project-creation'),
    url(r'^crear-md-proyecto-nor/$', NormalMetadataView.as_view(), name='crear-md-proyecto-nor'),
    url(r'^crear-proyecto-paralelo/$', ParallelProjectView.as_view(), name='parallel-project-creation'),
    url(r'^crear-md-proyecto-par/$', ParallelMetadataView.as_view(), name='crear-md-proyecto-par'),
    url(r'^rel-doc-metadato/$', DocNormalMetaRelationView.as_view(), name='rel-doc-metadato'),
    url(r'^rel-paralelo/$', ParallelRelationView.as_view(), name='rel-paralelo'),
    url(r'^rel-paral-rel-md/$', ParallelRelationView.as_view(), name='rel-paral-rel-md'),
    url(r'^borrar-proyecto/$', RemoveNormalProjectView.as_view(), name='delete-project'),
    url(r'^borrar-documento/$', RemoveDocumentView.as_view(), name='delete-document'),
    url(r'^borrar-md-proyecto-nor/$', RemoveNormalMetadataView.as_view(), name='delete-md-project-nor'),
    url(r'^borrar-proyecto-paralelo/$', RemoveParallelProjectView.as_view(), name='delete-parallel-project'),
    url(r'^borrar-md-proyecto-par/$', RemoveParallelMetadataView.as_view(), name='delete-md-project-par'),
    url(r'^borrar-doc-nor-meta-rel/$', RemoveDocNormalMetaRelationView.as_view(), name='delete-doc-nor-meta-rel'),
    url(r'^borrar-doc-par-meta-rel/$', RemoveRelationParallelMetaRelationView.as_view(), name='delete-doc-par-meta-rel'),
    url(r'^borrar-rel-paralelo/$', RemoveParallelRelationView.as_view(), name='delete-rel-parallel'),
    url(r'^cambiar-status-proyn', ChangeStatusNormalProjectView.as_view(), name='cambiar-status-proyn'),
    url(r'^cambiar-status-proyp', ChangeStatusParallellProjectView.as_view(), name='cambiar-status-proyp'),
    url(r'^list-docs-proy', ListFilesProjectView.as_view(), name='list-docs-proy'),
    url(r'^list-proy-own', ListProyectsOwnView.as_view(), name='list-proy-own'),
    url(r'^add-collab-proy', AddCollaboratorNormalProjectView.as_view(), name='add-collab-proy'),
    url(r'^pos-tag-file', PoSTagDocView.as_view(), name='pos-tag-file'),
    url(r'^download-file', DownloadFileView.as_view(), name='download-file'),
    url(r'^get-proy-md', GetMDProjectView.as_view(), name='get-proy-md'),
    url(r'^uptdate-doc', UpdateDocumentView.as_view(), name='update-doc'),
    url(r'^guardar-metadatos-documento', PushMDView.as_view(), name='guardar-metadatos-documento'),


]

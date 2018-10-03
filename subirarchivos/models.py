from django.conf import settings
from django.db import models

# Create your models here.
class NormalProject(models.Model):
    name = models.CharField(max_length=20, null=False, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner_normalproject', on_delete=models.CASCADE)
    project_members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    public_status = models.BooleanField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def is_public(self):
        return bool(self.public_status)

    def get_project_members(self):
        return self.project_members

    def get_owner(self):
        return self.owner

    def set_status(self, status):
        self.status=status

    def __str__(self):
        return str(self.name)

class Document(models.Model):
    file = models.FileField(blank=False, null=False, upload_to='mediafiles/')
    name = models.CharField(max_length=20, null=False, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='owner_document', on_delete=models.CASCADE)
    project = models.ForeignKey(NormalProject, related_name='project_document', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class NormalMetadata(models.Model):
    name = models.CharField(max_length=20, null=False)
    project = models.ForeignKey(NormalProject, related_name='project_normalMetadata', on_delete=models.CASCADE)

class DocumentNormalMetadataRelation(models.Model):
    metadata = models.ForeignKey(NormalMetadata, related_name='metadata', on_delete=models.CASCADE)
    document = models.ForeignKey(Document, related_name='document', on_delete=models.CASCADE)
    data = models.CharField(max_length=20, blank=True, null=True)

class ParallelRelation(models.Model):
    doc_one = models.ManyToManyField(Document, related_name='doc_one')
    doc_two = models.ManyToManyField(Document, related_name='doc_two')

class ParallelProject(models.Model):
    name = models.CharField(max_length=20, null=False, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner_parallelproject', on_delete=models.CASCADE)
    project_members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    relations = models.ManyToManyField(ParallelRelation)
    public_status = models.BooleanField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def is_public(self):
        return bool(self.public_status)

    def get_project_members(self):
        return self.project_members

    def __str__(self):
        return str(self.name)

class ParallelMetadata(models.Model):
    name = models.CharField(max_length=20, null=False)
    project = models.ForeignKey(ParallelProject, related_name='project_parallelmetadata', on_delete=models.CASCADE)

class DocumentParallelMetadaRelation(models.Model):#falta
    metadata = models.ForeignKey(ParallelMetadata, related_name="parallelmetadata", on_delete=models.CASCADE)
    relation = models.ForeignKey(ParallelRelation, related_name="relation", on_delete=models.CASCADE)
    data = models.CharField(max_length=20, blank=True, null=True)

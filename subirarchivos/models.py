from django.conf import settings
from django.db import models

# Create your models here.
class NormalProject(models.Model):
    name = models.CharField(max_length=20, null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner_normalproject', on_delete=models.CASCADE)
    project_members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    public_status = models.BooleanField(default=0)

    def is_public(self):
        return bool(self.public_status)

class Document(models.Model):
    file = models.FileField(blank=False, null=False)
    name = models.CharField(max_length=20, null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='owner_document', on_delete=models.CASCADE)
    project = models.ForeignKey(NormalProject, related_name='project_document', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class NormalMetadata(models.Model):
    name = models.CharField(max_length=20, null=False)
    data = models.CharField(max_length=20, null=False)
    project = models.ForeignKey(NormalProject, related_name='project_normalMetadata', on_delete=models.CASCADE)

class ParallelRelation(models.Model):
    doc_one = models.ManyToManyField(Document, related_name='doc_one')
    doc_two = models.ManyToManyField(Document, related_name='doc_two')

class ParallelProject(models.Model):
    name = models.CharField(max_length=20, null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owner_parallelproject', on_delete=models.CASCADE)
    project_members = models.ManyToManyField(settings.AUTH_USER_MODEL)
    relation = models.ManyToManyField(ParallelRelation)
    public_status = models.BooleanField(default=0)

    def is_public(self):
        return bool(self.public_status)

class ParallelMetadata(models.Model):
    name = models.CharField(max_length=20, null=False)
    data = models.CharField(max_length=20, null=False)
    project = models.ForeignKey(ParallelProject, related_name='project_parallelmetadata', on_delete=models.CASCADE)

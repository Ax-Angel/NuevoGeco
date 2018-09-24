from rest_framework import serializers
from .models import Document, NormalProject, NormalMetadata, ParallelRelation, ParallelProject, ParallelMetadata

class DocumentSerializer(serializers.ModelSerializer):
    class Meta():
        model = Document
        fields = ('file', 'name', 'timestamp')

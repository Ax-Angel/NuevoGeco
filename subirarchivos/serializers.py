from rest_framework import serializers
#from .models import Document, NormalProject, NormalMetadata, ParallelRelation, ParallelProject, ParallelMetadata
from .models import *

class CreateUserSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, allow_blank=False, trim_whitespace=True)
    user_name = serializers.CharField(max_length=20, allow_blank=False, trim_whitespace=False)
    password = serializers.CharField(max_length=20, allow_blank=False, trim_whitespace=False)

class NormalProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = NormalProject
        fields = ('name', )

class DocumentSerializer(serializers.Serializer):
    file = serializers.FileField()
    project = serializers.CharField(max_length=30, allow_blank=False, trim_whitespace=False)

# Hecho por Diego... Cualquier cosa, avísame.
class NormalMetadataSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20, allow_blank=False, trim_whitespace=True)
    project = serializers.CharField(max_length=30, allow_blank=False, trim_whitespace=False)

class ParallelProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParallelProject
        fields = ('name', )

class ParallelMetadataSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20, allow_blank=False, trim_whitespace=True)
    project = serializers.CharField(max_length=30, allow_blank=False, trim_whitespace=True)

class DocNormalMetaRelationSerializer(serializers.Serializer):
    project = serializers.CharField(max_length=20, allow_blank=False, trim_whitespace=True)
    metadata = serializers.CharField(max_length=20, allow_blank=False, trim_whitespace=True)
    document = serializers.CharField(max_length=20, allow_blank=False, trim_whitespace=True)
    data = serializers.CharField(max_length=20, allow_blank=False, trim_whitespace=True)

class ParallelRelationSerializer(serializers.Serializer):
    doc1 = serializers.FileField()
    doc2 = serializers.FileField()
    project = serializers.CharField(max_length=20, allow_blank=False, trim_whitespace=True)

class ParallelRelationParallelMetadataRelation(serializers.Serializer):
    project = serializers.CharField(max_length=20, allow_blank=False, trim_whitespace=True)
    metadata = serializers.CharField(max_length=20, allow_blank=False, trim_whitespace=True)
    relation = serializers.CharField(max_length=20, allow_blank=False, trim_whitespace=True)
    data = serializers.CharField(max_length=20, allow_blank=False, trim_whitespace=True)

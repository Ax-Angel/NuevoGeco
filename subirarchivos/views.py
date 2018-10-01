from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.models import User

from .serializers import *
from .models import *

# Create your views here.
class CreateUserView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny, )
    def post(self, request, *args, **kwargs):
        project_serializer = CreateUserSerializer(data=request.data)
        if project_serializer.is_valid():
            validatedData = project_serializer.validated_data
            print(validatedData)

            usr = User.objects.create_user(username = str(validatedData['user_name']),
                                                email = str(validatedData['email']),# misma respuesta
                                                password = str(validatedData['password']),
                                                )

            return Response(project_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NormalProjectView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        project_serializer = NormalProjectSerializer(data=request.data)
        if project_serializer.is_valid():
            validatedData = project_serializer.validated_data
            print(validatedData)

            project = NormalProject(owner = request.user,
                                            name = str(validatedData['name']),
                                            )
            project.save()
            project.project_members.add(request.user)
            return Response(project_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        file_serializer = DocumentSerializer(data=request.data)
        if file_serializer.is_valid():
            validatedData = file_serializer.validated_data
            print(validatedData)
            print(request.user.id)

            projectObj = NormalProject.objects.get(name = str(validatedData['project']))
            users = projectObj.get_project_members().all()
            if request.user in users.all():

                doc = Document(file = validatedData['file'],
                                    name = str(validatedData['file']),
                                    owner = request.user,
                                    project = projectObj,

                                    )
                doc.save()

                    #Response("{\"name\": \"name already exists\"}", status=status.HTTP_400_BAD_REQUEST)
            else:
                print("sin permisos")
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Hecho por Diego... Cualquier cosa que estuvo, avísame.
class NormalMetadataView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        metadata_serializer = NormalMetadataSerializer(data=request.data)
        if metadata_serializer.is_valid():
            validatedData = metadata_serializer.validated_data

            projectObj = NormalProject.objects.get(name = str(validatedData['project']))
            users = projectObj.get_project_members().all()

            if request.user in users.all():
                metadata = NormalMetadata(name = str(validatedData['name']),
                                             project = projectObj,

                                )
                metadata.save()
            else:
                print("sin permisos")
            return Response(metadata_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(metadata_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParallelProjectView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        parallel_project_serializer = ParallelProjectSerializer(data=request.data)
        if parallel_project_serializer.is_valid():
            validatedData = parallel_project_serializer.validated_data

            project = ParallelProject(owner = request.user,
                                        name = str(validatedData['name']),

                                        )
            project.save()
            project.project_members.add(request.user)
            return Response(parallel_project_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(parallel_project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParallelMetadataView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        parallel_metadata_serializer = ParallelMetadataSerializer(data=request.data)
        if parallel_metadata_serializer.is_valid():
            validatedData = parallel_metadata_serializer.validated_data

            projectObj = NormalProject.objects.get(name = str(validatedData['project']))
            users = projectObj.get_project_members().all()

            if request.user in users.all():
                p_metadata = ParallelMetadata(name = str(validatedData['name']),
                                                project = projectObj,
                                )
                p_metadata.save()
            else:
                print("sin permisos")
            return Response(parallel_metadata_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(parallel_metadata_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocNormalMetaRelationView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        doc_meta_serializer = DocNormalMetaRelationSerializer(data=request.data)
        if doc_meta_serializer.is_valid():
            validatedData = doc_meta_serializer.validated_data

            projectObj = NormalProject.objects.get(name = str(validatedData['project']))
            users = projectObj.get_project_members().all()

            if request.user in users.all():
                relation = DocumentNormalMetadataRelation(metadata = validatedData['metadata'],
                                                            document = validatedData['document'],
                                                            data = validatedData['data'],
                                                            )
                relation.save()
            else:
                print("sin permisos")
            return Response(doc_meta_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(doc_meta_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class ParallelRelationView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        parallel_serializer = ParallelRelationSerializer(data=request.data)
        if parallel_serializer.is_valid():
            validatedData = parallel_serializer.validated_data

            # Tengo duda, debo obtener los dos documentos?
            projectObj = NormalProject.objects.get(name = str(validatedData['project']))
            users = projectObj.get_project_members().all()

            if request.user in users.all():
                parallel_relation = ParallelRelation(doc1 = validatedData['doc1'],
                                                        doc2 = validatedData['doc2'],
                                                            )
                parallel_relation.save()
            else:
                print("sin permisos")
            return Response(parallel_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(parallel_serializer.data, status=status.HTTP_400_BAD_REQUEST)



class DocNormalMetaRelationView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        doc_meta_serializer = ParallelRelationParallelMetadataRelation(data=request.data)
        if doc_meta_serializer.is_valid():
            validatedData = doc_meta_serializer.validated_data

            projectObj = NormalProject.objects.get(name = str(validatedData['project']))
            users = projectObj.get_project_members().all()

            if request.user in users.all():
                relation = DocumentNormalMetadataRelation(metadata = validatedData['metadata'],
                                                            relation = validatedData['relation'],
                                                            data = validatedData['data'],
                                                            )
                relation.save()
            else:
                print("sin permisos")
            return Response(doc_meta_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(doc_meta_serializer.data, status=status.HTTP_400_BAD_REQUEST)

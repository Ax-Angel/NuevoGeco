from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.models import User
from django.http import JsonResponse

from .serializers import *
from .models import *

# Create your views here.
class CreateUserView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny, )
    def post(self, request, *args, **kwargs):
        user_serializer = CreateUserSerializer(data=request.data)
        if user_serializer.is_valid():
            validatedData =     user_serializer.validated_data
            #print(validatedData)

            try:
                usr = User.objects.create_user(username = str(validatedData['user_name']),
                                                email = str(validatedData['email']),# misma respuesta
                                                password = str(validatedData['password']),
                                                )
                print(user_serializer.data)
                return Response(user_serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return JsonResponse({"error": "El nombre de usuario o correo ya existe"}, status=status.HTTP_409_CONFLICT)

        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NormalProjectView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        project_serializer = NormalProjectSerializer(data=request.data)
        if project_serializer.is_valid():
            validatedData = project_serializer.validated_data
            print(validatedData)

            try:
                project = NormalProject(owner = request.user,
                                            name = str(validatedData['name']),
                                            )
                project.save()
                project.project_members.add(request.user)
                return Response(project_serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return JsonResponse({"error": "El nombre del proyecto ya existe"}, status=status.HTTP_409_CONFLICT)
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
                try:
                    doc = Document(file = validatedData['file'],
                                        name = str(validatedData['file']),
                                        owner = request.user,
                                        project = projectObj,

                                        )
                    try:
                        doc.save()
                        return Response(file_serializer.data, status=status.HTTP_201_CREATED)
                    except:
                        return JsonResponse({"error": "El formato del archivo no es valido"}, status=status.HTTP_409_CONFLICT)
                except IntegrityError as e:
                    return JsonResponse({"error": "El nombre del documento ya existe"}, status=status.HTTP_409_CONFLICT)
            else:
                print("sin permisos")
                return JsonResponse({"error": "El usuario no tiene permisos para hacer esta accion"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                return Response(metadata_serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("sin permisos")
                return JsonResponse({"error": "El usuario no tiene permisos para hacer esta accion"}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(metadata_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParallelProjectView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        parallel_project_serializer = ParallelProjectSerializer(data=request.data)
        if parallel_project_serializer.is_valid():
            validatedData = parallel_project_serializer.validated_data
            try:
                project = ParallelProject(owner = request.user,
                                            name = str(validatedData['name']),

                                            )
                project.save()
                project.project_members.add(request.user)
                return Response(parallel_project_serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                return JsonResponse({"error": "El nombre del proyecto paralelo ya existe"}, status=status.HTTP_409_CONFLICT)
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
                return Response(parallel_metadata_serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("sin permisos")
                return JsonResponse({"error": "El usuario no tiene permisos para hacer esta accion"}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(parallel_metadata_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#aqui me quedeeeeeeeeeeeeee
class DocNormalMetaRelationView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        doc_meta_serializer = DocNormalMetaRelationSerializer(data=request.data)
        if doc_meta_serializer.is_valid():
            validatedData = doc_meta_serializer.validated_data

            projectObj = NormalProject.objects.get(name = str(validatedData['project']))
            users = projectObj.get_project_members().all()
            document = Document.objects.get(name = validatedData['document'], project = projectObj)
            metadata = NormalMetadata.objects.get(name = validatedData['metadata'])
            if projectObj is not None and document is not None and metadata is not none:
                if request.user in users.all():
                    relation = DocumentNormalMetadataRelation(metadata = metadata,
                                                                document = document,
                                                                data = validatedData['data'],
                                                                )
                    relation.save()
                    return Response(doc_meta_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    print("sin permisos")
                    return JsonResponse({"error": "El usuario no tiene permisos para hacer esta accion"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return JsonResponse({"error": "El proyecto, documento o metadato, no fueron encontrados"}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response(doc_meta_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParallelRelationView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        parallel_serializer = ParallelRelationSerializer(data=request.data)
        if parallel_serializer.is_valid():
            validatedData = parallel_serializer.validated_data

            projectObj = NormalProject.objects.get(name = str(validatedData['project']))
            users = projectObj.get_project_members().all()
            doc1 = Document.objects.get(name = validatedData['doc1'])
            doc2 = Document.objects.get(name = validatedData['doc2'])
            if projectObj and doc1 and doc2:
                if request.user in users.all():
                    parallel_relation = ParallelRelation(doc1 = doc1,
                                                            doc2 = doc2,
                                                                )
                    parallel_relation.save()
                    return Response(parallel_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    print("sin permisos")
                    return JsonResponse({"error": "El usuario no tiene permisos para hacer esta accion"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return JsonResponse({"error": "El proyecto, documento 1 o documento 2, no fueron encontrados"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(parallel_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DocParallelMetaRelationView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        doc_meta_serializer = ParallelRelationParallelMetadataSerializer(data=request.data)
        if doc_meta_serializer.is_valid():
            validatedData = doc_meta_serializer.validated_data

            projectObj = NormalProject.objects.get(name = str(validatedData['project']))
            users = projectObj.get_project_members().all()
            metadata = ParallelMetadata.objects.get(name = validatedData['metadata'])
            relation = ParallelRelation.objects.get(name = validatedData['relation'])
            if projectObj and metada and relation:
                if request.user in users.all():
                    relation = DocumentNormalMetadataRelation(metadata = metadata,
                                                                relation = relation,
                                                                data = validatedData['data'],
                                                                )
                    relation.save()
                    return Response(doc_meta_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    print("sin permisos")
                    return JsonResponse({"error": "El usuario no tiene permisos para hacer esta accion"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return JsonResponse({"error": "El proyecto, metadato o relacion, no fueron encontrados"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(doc_meta_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveNormalProjectView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        rm_project_serializer = RemoveNormalProjectSerializer(data=request.data)
        if rm_project_serializer.is_valid():
            validatedData = rm_project_serializer.validated_data

            projectObj = NormalProject.objects.get(name = str(validatedData['name']))
            owner = projectObj.get_owner().all()
            if request.user in owner:
                project = NormalProject.objects.get(name=validatedData['name'])
                if project is not None:
                    project.delete()
                    return Response(rm_project_serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return JsonResponse({"error": "El proyecto no fue encontrado"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse({"error": "El usuario no tiene permiso para realizar esta accion"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(rm_project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveDocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        rm_file_serializer = RemoveDocumentSerializer(data=request.data)
        if rm_file_serializer.is_valid():
            validatedData = rm_file_serializer.validated_data

            projectObj = NormalProject.objects.get(name = str(validatedData['project']))
            users = projectObj.get_project_members().all()
            if request.user in users.all():
                doc = Document.objects.get(name=validatedData['name'])
                if doc is not None:
                    doc.delete()
                    return Response(rm_file_serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return JsonResponse({"error": "El documento no fue encontrado"}, status=status.HTTP_404_NOT_FOUND)
            else:
                print("sin permisos")
                return JsonResponse({"error": "El usuario no tiene permiso para realizar esta accion"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(rm_file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveNormalMetadataView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        rm_metadata_serializer = RemoveNormalMetadataSerializer(data=request.data)
        if rm_metadata_serializer.is_valid():
            validatedData = rm_metadata_serializer.validated_data

            projectObj = NormalProject.objects.get(name = str(validatedData['project']))
            users = projectObj.get_project_members().all()

            if request.user in users.all():
                metadata = NormalMetadata.objects.get(name=validatedData['name'])
                if metadata is not None:
                    metadata.delete()
                    return Response(rm_metadata_serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return JsonResponse({"error": "El metadato no fue encontrado"}, status=status.HTTP_404_NOT_FOUND)
            else:
                print("sin permisos")
                return JsonResponse({"error": "El usuario no tiene permiso para realizar esta accion"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(rm_metadata_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RemoveParallelProjectView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        rm_project_serializer = RemoveParallelProjectSerializer(data=request.data)
        if rm_project_serializer.is_valid():
            validatedData = rm_project_serializer.validated_data

            projectObj = NormalProject.objects.get(name = str(validatedData['name']))
            owner = projectObj.get_owner().all()
            if request.user in owner:
                project = ParallelProject.objects.get(name=validatedData['name'])
                if project is not None:
                    project.delete()
                    return Response(rm_project_serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return JsonResponse({"error": "El proyecto no fue encontrado"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse({"error": "El usuario no tiene permiso para realizar esta accion"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(rm_project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveParallelMetadataView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        rm_metadata_serializer = RemoveParallelMetadataSerializer(data=request.data)
        if rm_metadata_serializer.is_valid():
            validatedData = rm_metadata_serializer.validated_data

            projectObj = NormalProject.objects.get(name = str(validatedData['project']))
            users = projectObj.get_project_members().all()

            if request.user in users.all():
                metadata = ParallelMetadata.objects.get(name=validatedData['name'])
                if metadata is not None:
                    metadata.delete()
                    return Response(rm_metadata_serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return JsonResponse({"error": "El metadato no fue encontrado"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse({"error": "El usuario no tiene permiso para realizar esta accion"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(rm_metadata_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveDocNormalMetaRelationView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        rm_doc_meta_serializer = RemoveDocNormalMetaRelationSerializer(data=request.data)
        if rm_doc_meta_serializer.is_valid():
            validatedData = rm_doc_meta_serializer.validated_data

            projectObj = NormalProject.objects.get(name = str(validatedData['project']))
            users = projectObj.get_project_members().all()

            if request.user in users.all():
                metadata = NormalMetadata.objects.get(name=validatedData['metadata'])
                document = Document.objects.get(name=validatedData['document'])
                if metadata is not None and document is not None:
                    relation = DocumentNormalMetadataRelation.objects.get(metadata=metadata, document=document)
                    relation.delete()
                    return Response(rm_doc_meta_serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return JsonResponse({"error": "El metadato o documento no fue encontrado"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse({"error": "El usuario no tiene permiso para realizar esta accion"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(rm_doc_meta_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveRelationParallelMetaRelationView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        rm_doc_par_rel_serializer = RemoveParallelRelationParallelMetadataSerializer(data=request.data)
        if rm_doc_par_rel_serializer.is_valid():
            validatedData = rm_doc_par_rel_serializer.validated_data

            projectObj = NormalProject.objects.get(name = str(validatedData['project']))
            users = projectObj.get_project_members().all()

            if request.user in users.all():
                metadata = ParallelMetadata.objects.get(name = str(validatedData['metadata']))
                doc1 = Document.objects.get(name=validatedData['doc1'])
                doc2 = Document.objects.get(name=validatedData['doc2'])
                relation = ParallelRelation.objects.get(doc1=doc1, doc2=doc2)
                if metadata is not None:
                    relation = DocumentParallelMetadaRelation.objects.get(metadata=metadata, relation=relation)
                    relation.delete()
                    return Response(rm_doc_par_rel_serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return JsonResponse({"error": "El metadato o la relacion no fue encontrado"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse({"error": "El usuario no tiene permiso para realizar esta accion"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(rm_doc_par_rel_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveParallelRelationView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        rm_parallel_rel_serializer = RemoveParallelRelationSerializer(data=request.data)
        if rm_parallel_rel_serializer.is_valid():
            validatedData = rm_parallel_rel_serializer.validated_data

            projectObj = NormalProject.objects.get(name = str(validatedData['project']))
            users = projectObj.get_project_members().all()

            if request.user in users.all():
                doc1 = Document.objects.get(name=validatedData['doc1'])
                doc2 = Document.objects.get(name=validatedData['doc2'])
                if doc1 is not None and doc2 is not None:
                    relation = ParallelRelation.objects.get(doc1=doc1, doc2=doc2)
                    relation.delete()
                    return Response(rm_parallel_rel_serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return JsonResponse({"error": "Alguno de los dos nombres de los documentos no fue encontrado"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse({"error": "El usuario no tiene permiso para realizar esta accion"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(rm_parallel_rel_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangeStatusNormalProjectView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        ch_status_serializer = ChangeStatusProjectSerializer(data=request.data)
        if ch_status_serializer.is_valid():
            validatedData = ch_status_serializer.validated_data

            projectObj = NormalProject.objects.get(name = str(validatedData['project']))
            owner = projectObj.get_owner().all()
            if projectObj:
                if request.user in owner:
                    if projectObj.is_public() == True:
                        projectObj.set_status(False)
                        return Response(ch_status_serializer, status=status.HTTP_202_ACCEPTED)
                    else:
                        projectObj.set_status(True)
                        return Response(ch_status_serializer, status=status.HTTP_202_ACCEPTED)
                else:
                    return JsonResponse({"error": "El usuario no tiene permiso para realizar esta accion"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return JsonResponse({"error": "El proyecto no fue encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(ch_status_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangeStatusParallellProjectView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        ch_status_serializer = ChangeStatusProjectSerializer(data=request.data)
        if ch_status_serializer.is_valid():
            validatedData = ch_status_serializer.validated_data

            projectObj = ParallelProject.objects.get(name = str(validatedData['project']))
            owner = projectObj.get_owner().all()
            if projectObj:
                if request.user in owner:
                    if projectObj.is_public() == True:
                        projectObj.set_status(False)
                        return Response(ch_status_serializer.data, status=status.HTTP_202_ACCEPTED)
                    else:
                        projectObj.set_status(True)
                        return Response(ch_status_serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return JsonResponse({"error": "El usuario no tiene permiso para realizar esta accion"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return JsonResponse({"error": "El proyecto no fue encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(ch_status_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListFilesProject(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated, )
    def post(self, request, *args, **kwargs):
        serializer = ListFilesProjectSerializer(data=request.data)
        if serializer.is_valid():
            validatedData = serializer.validated_data

            projectObj = NormalProject.objects.get(name = str(validatedData['project']))
            if projectObj:
                users = projectObj.get_project_members().all()
                if request.user in users.all():
                    documents_set = Document.objects.filter(project = projectObj)
                    documents = []
                    for doc in documents_set:
                        documents.append(doc.name)
                    return JsonResponse({"Documentos": documents}, status=status.HTTP_202_ACCEPTED)
                else:
                    return JsonResponse({"error": "El usuario no tiene permiso para realizar esta accion"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return JsonResponse({"error": "El proyecto no fue encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(ch_status_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

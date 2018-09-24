from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .serializers import DocumentSerializer

# Create your views here.
#class DocumentView(APIView):
#	parser_classes = (MultiPartParser, FormParser)
#	def post(self, request, *args, **kwargs):
#		file_serializer = DocumentSerializer(data=request.data)
#		if file_serializer.is_valid():
#           validatedData = file_serializer.validated_data
#
#			return Response(file_serializer.data, status=status.HTTP_201_CREATED)
#		else:
#			return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

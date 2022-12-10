from dotenv import load_dotenv
import os
from azure.storage.blob import BlobClient
from django.http import  JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
import uuid

load_dotenv()
CONNECTION_STRING = os.environ.get("CONNECTION_STRING")
CONTAINER_NAME = os.environ.get("CONTAINER_NAME")

def uploadFile(file):
    
    filename=str(uuid.uuid4())
    blob = BlobClient.from_connection_string(conn_str=CONNECTION_STRING,container_name = CONTAINER_NAME ,blob_name=filename)
    blob.upload_blob(file.read())
    return filename

def fileUrl(filename):
    blob=BlobClient.from_connection_string(conn_str=CONNECTION_STRING,container_name = CONTAINER_NAME ,blob_name=filename)
    return blob.url


class cropter(APIView):

    def post(self,request):
        image = request.data['image']
        if(image is None):
            return Response('Invalid Input')
        filename=None
        if(image):
            filename=uploadFile(image)
        return JsonResponse({'display_url':fileUrl(filename)})
    
    def get(self,request,filename,format=None):
        return JsonResponse({'display_url':fileUrl(filename)})



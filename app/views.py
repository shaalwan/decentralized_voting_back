from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework import status,viewsets
from django.http.response import Http404
# Create your views here.()

from .models import *
from .serializers import *

class voterRegister(APIView):
  def post(self,request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    aadhar = request.POST.get('aadhar')
    election_address = request.POST.get('election')

    user = User.objects.create_user(email,password)
    user.save()

    voter = Voter(user = user,aadhar = aadhar,election_address = election_address)
    voter.save()

    serialzier = VoterSerializer(voter)
    return Response(serialzier.data)

class companyRegister(APIView):
  def post(self,request):

    email = request.POST.get('email')
    password = request.POST.get('password')
    
    company = User.objects.create_user(email,password)
    company.is_company = True
    company.save()

    serializer = userSerializer(company)
    return Response(serializer.data)

class voterAuthenticate(APIView):
  def post(self, request, format=None):
        data = request.data
        email = data['email']
        password = data['password']
        user = authenticate(username=email, password=password)

        if user is not None :
            id = user.pk
            if user.is_company == False:
                voter = Voter.objects.get(user_id = id)
                serialzier = VoterSerializer(voter)
                return Response(serialzier.data)
            return Response({"Error": "not a voter"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Error": "invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class companyAuthenticate(APIView):
  def post(self, request, format=None):
        data = request.data
        email = data['email']
        password = data['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_company == True:
                serializer = userSerializer(user)
                return Response(serializer.data)
            return Response({"Error": "not a company"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Error": "invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class voterList(viewsets.ReadOnlyModelViewSet):
    model = Voter
    serializer_class = VoterSerializer
    def get_queryset(self):
        voters = Voter.objects.all()
        return voters

class voter(APIView):

    def get_object(self, pk):
        try:
            user = User.objects.get(pk=pk)
            if(user.is_company==False):
                return Voter.objects.get(user_id = user.pk)
            return Http404
        except Voter.DoesNotExist:
            raise Http404

    def get(self, requests, pk):
        voter = self.get_object(pk)
        serializer = VoterSerializer(voter)
        return Response(serializer.data)

    def put(self, requests, pk):
        voter = self.get_object(pk)
        serializer = VoterSerializer(voter, data=requests.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, requests, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class electionlist(viewsets.ReadOnlyModelViewSet):
    model = Election
    serializer_class = electionSerializer

    def get_queryset(self):
        elections = Election.objects.filter(user=self.request.user.id)
        return elections
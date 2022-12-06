from rest_framework import serializers

from django.db.models import fields
from django.db.models.query import prefetch_related_objects
from rest_framework.compat import apply_markdown
from .models import *
from rest_framework.validators import UniqueValidator


class userSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id','email','is_company']

class VoterSerializer(serializers.ModelSerializer):
  user = userSerializer()
  class Meta:
    model = Voter
    fields = ['user','aadhar','election_address']
  
class electionSerializer(serializers.ModelSerializer):
  user = userSerializer()
  class Meta:
    model = Election
    fields = ['user','election']
    
